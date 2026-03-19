"""
Chamaroma Studio FastAPI Backend
Complete integration: Editor de Prompts/Imagens + Catálogo 17 Aromas + Copy Raio-X + Video/Instagram
Powered by Google Gemini (ZERO dependência de Claude/Anthropic)
"""

import os
import sys
import time
import base64
import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from io import BytesIO
from enum import Enum

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

# Load environment variables from parent and current directory
parent_env = Path(__file__).parent.parent / ".env"
current_env = Path(__file__).parent / ".env"

if parent_env.exists():
    load_dotenv(parent_env)
if current_env.exists():
    load_dotenv(current_env)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
ALLOWED_ORIGINS.append("*")

# Initialize Gemini client
gemini_client = None
if genai and GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Import data modules (will be in data/ directory)
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from data.catalogo_aromas import get_all_aromas, get_aroma_by_id, Aroma
except ImportError:
    # Fallback mock data if modules not available
    class Aroma:
        def __init__(self, id: str, name: str, description: str, notas: List[str]):
            self.id = id
            self.name = name
            self.description = description
            self.notas = notas

        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "notas": self.notas
            }

    AROMAS_DB = {
        "lavanda": Aroma("lavanda", "Lavanda Premium", "Essência pura de lavanda francesa", ["floral", "herbáceo", "relaxante"]),
        "canela": Aroma("canela", "Canela & Especiarias", "Blend quente de canela e cravos", ["especiaria", "quente", "aconchego"]),
        "jasmim": Aroma("jasmim", "Jasmim Noturno", "Jasmim indiano exótico", ["floral", "noturno", "sedutora"]),
        "coco": Aroma("coco", "Coco & Baunilha", "Tropical e doce", ["tropical", "doce", "acomodante"]),
        "menta": Aroma("menta", "Menta Fresca", "Menta refrescante", ["herbáceo", "fresco", "energizante"]),
        "rosa": Aroma("rosa", "Rosa Vermelha", "Rosa clássica", ["floral", "elegante", "sofisticado"]),
        "limao": Aroma("limao", "Limão Siciliano", "Cítrico vibrante", ["cítrico", "fresco", "revigorante"]),
        "mogno": Aroma("mogno", "Mogno & Sândalo", "Madeira profunda", ["amadeirado", "quente", "luxuoso"]),
        "gardenia": Aroma("gardenia", "Gardênia Branca", "Flor branca pura", ["floral", "delicado", "feminino"]),
        "gengibre": Aroma("gengibre", "Gengibre Picante", "Especiaria vibrante", ["especiaria", "quente", "energético"]),
        "ambar": Aroma("ambar", "Âmbar & Musgo", "Âmbar quente", ["amadeirado", "quente", "sofisticado"]),
        "cafe": Aroma("cafe", "Café & Chocolate", "Blend aromático", ["café", "chocolate", "aconchegante"]),
        "cereja": Aroma("cereja", "Cereja Negra", "Frutal intenso", ["frutal", "intenso", "sedutor"]),
        "eucalipto": Aroma("eucalipto", "Eucalipto Mentolado", "Revigorante", ["herbáceo", "mentolado", "refrescante"]),
        "baunilha": Aroma("baunilha", "Baunilha Madagascar", "Clássica doce", ["doce", "quente", "clássico"]),
        "vetiver": Aroma("vetiver", "Vetiver Terroso", "Terroso e profundo", ["amadeirado", "terroso", "sofisticado"]),
        "yuzu": Aroma("yuzu", "Yuzu Japonês", "Cítrico singular", ["cítrico", "fresco", "sofisticado"]),
    }

    def get_all_aromas():
        return list(AROMAS_DB.values())

    def get_aroma_by_id(aroma_id: str):
        return AROMAS_DB.get(aroma_id)

# FastAPI app initialization
app = FastAPI(
    title="Chamaroma Studio API",
    description="Editor de Prompts/Imagens + Catálogo 17 Aromas + Copy Raio-X + Video/Instagram",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for logos
logos_dir = Path(__file__).parent / "logos"
if logos_dir.exists():
    app.mount("/logos", StaticFiles(directory=str(logos_dir)), name="logos")


# ============================================================================
# ANTI-CLICHE GLOBAL DIRECTIVE
# ============================================================================
ANTI_CLICHE_DIRECTIVE = """
PROIBIDO: banheiras, livros, xícaras, camas/lençóis, fairy lights, suculentas, spa, yoga, casais stock photo, fundos genéricos, luz soft sem direção, mãos sem intenção.
PROIBIDO TEXTUAL: "transforme seu ambiente", "momentos especiais", "aconchego do lar".
REGRA: se parece Pinterest 2018 ou catálogo genérico, NÃO FAÇA. Cada prompt = decisão criativa única.
PREFERIR: concreto, metal oxidado, madeira crua, contrastes extremos, iluminação intencional, editorial.
"""

# ============================================================================
# 10 PROMPT SYSTEM DEFINITIONS
# ============================================================================
PROMPT_SYSTEM = {
    "hero_shot": """Fundo #FFFFFF ciclorama. Produto 70-80% frame, ângulo 3/4. Key 45°, fill 30%, rim. Tack-sharp 8K. 100% fiel. Velas: 3200K+5600K, textura cera.""",
    "dark_moody": """Chiaroscuro: produto como ÚNICA LUZ em escuridão total. Caravaggio. Âmbar/dourado/cobre. Pool de cera refletindo chama. Fundo negro absoluto. f/1.8, 8K.""",
    "ingredient_story": """Produto + ingredientes CRUS macro ao nível do solo: coco, canela, lavanda (conforme aroma). Conexão matéria-prima/produto. Luz natural janela alta. Editorial artesanal.""",
    "lifestyle": """Momento de uso REAL: pessoa real acendendo vela/borrifando spray. Cena cotidiana, imperfeições. Produto é coadjuvante. Rosto fora de quadro. Ação natural, não posada.""",
    "anti_cliche": """Contexto INESPERADO: concreto bruto rachado | synth vintage | bancada marcenaria | muro grafitado. Contraste artesanal vs brutal. Zero styling. Ângulo oblíquo baixo. Zine editorial.""",
    "ambience": """Produto em ambiente REAL decorado: sala contemporânea, cozinha industrial, varanda. Produto é parte da composição. Design de interiores editorial (Arch Digest / Casa Vogue).""",
    "close_up": """Macro EXTREMO: textura cera, pool derretida, fibras pavio, rótulo em foco. f/1.4-2.0, bokeh cremoso. Revela craftsmanship. Hasselblad macro 8K.""",
    "social_media": """Flat lay OVERHEAD geométrico. Produto + 4-6 elementos (ingredientes secos, linho, botânico). Fundo texturizado (concreto/mármore/linho — NUNCA branco liso). Pronto para post.""",
    "smoke_aroma": """Sinestesia: fragrância visível. Fumaça/névoa + elementos do aroma flutuando (pétalas, canela). Contraluz backlit, fundo escuro. Para spray: névoa freeze com micro-gotículas.""",
    "premium_context": """Produto como arte: pedestal galeria, mármore Calacatta, ônix negro. Iluminação museu, spots cirúrgicos. Espaço negativo. Ref: Aesop/Le Labo/Byredo. Monumental.""",
}

# ============================================================================
# CATEGORY RULES
# ============================================================================
CATEGORY_RULES = {
    "velas": {
        "description": "Velas Aromáticas - use dados do catálogo de aromas",
        "enrich_with_aroma": True,
        "rules": [
            "Destacar textura da cera",
            "Mostrar pool de cera derretida quando acesa",
            "Mencionar notas aromáticas do catálogo"
        ]
    },
    "home_spray": {
        "description": "Home Spray - fotografia com mist e elementos flutuantes",
        "rules": [
            "Capturar névoa em suspensão (freeze photography)",
            "Micro-gotículas visíveis em contraluz",
            "Elementos aromáticos flutuando (pétalas, especiarias)",
            "Fundo escuro para contraste da névoa"
        ]
    }
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================
class AromaResponse(BaseModel):
    id: str
    name: str
    description: str
    notas: List[str]


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    aroma_count: int
    timestamp: str


class GeneratePromptsRequest(BaseModel):
    category: str
    image_url: str  # base64 or URL
    name_size: str
    hex_code: Optional[str] = None
    aroma: Optional[str] = None
    mode: str = "flash"  # flash or pro


class GeneratedPrompts(BaseModel):
    category: str
    product_name: str
    prompts: Dict[str, str]
    aroma_data: Optional[Dict] = None


class GenerateImageRequest(BaseModel):
    prompt: str
    model: str = "flash"  # flash or pro
    aspect_ratio: str = "1:1"  # 1:1, 9:16, 16:9
    reference_image: Optional[str] = None  # base64
    watermark: Optional[str] = None  # brand name


class GenerateImageResponse(BaseModel):
    image_base64: str
    model: str
    aspect_ratio: str


class VideoScriptsRequest(BaseModel):
    product_name: str
    category: str
    product_brand: str
    content_for: str
    selected_images: List[str]
    mode: str = "flash"


class VideoScriptsResponse(BaseModel):
    clips_ml: List[Dict]
    instagram_feed: List[Dict]
    instagram_stories: List[Dict]


class VideoNarrationRequest(BaseModel):
    product_name: str
    category: str
    product_brand: str
    hero_shot: str
    lifestyle: str
    dark_moody: str
    smoke_aroma: str
    content_for: str
    mode: str = "flash"


class VideoNarrationResponse(BaseModel):
    narracao: str


class InstagramPostRequest(BaseModel):
    product_name: str
    category: str
    product_brand: str
    prompts: Optional[Dict] = None
    generated_image_keys: Optional[List[str]] = None
    mode: str = "flash"


class InstagramPostResponse(BaseModel):
    post_type: str
    caption: str
    hashtags: List[str]
    slides: List[Dict]
    best_posting_time: str
    content_pillar: str
    cta_type: str
    alt_text: str


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def retry_gemini_call(func, max_retries=3, backoff_delays=[2, 4, 8]):
    """Retry logic with exponential backoff for Gemini API calls."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                delay = backoff_delays[attempt]
                time.sleep(delay)
            else:
                raise


def extract_base64_from_data_url(data_url: str) -> str:
    """Extract base64 string from data:image/... URL."""
    if data_url.startswith("data:"):
        return data_url.split(",", 1)[1]
    return data_url


def add_watermark_to_image(image_data: bytes, brand_name: str) -> bytes:
    """Add watermark logo to image using PIL."""
    if not Image:
        return image_data

    try:
        # Load image
        img = Image.open(BytesIO(image_data)).convert("RGBA")

        # Load logo
        logo_mapping = {
            "chamaroma": "chamaroma.png",
            "aquinobrasil": "aquinobrasil.png",
            "gama": "gama.png",
            "labor": "labor.png",
        }

        logo_filename = logo_mapping.get(brand_name.lower(), "chamaroma.png")
        logo_path = Path(__file__).parent / "logos" / logo_filename

        if not logo_path.exists():
            return image_data

        # Load and resize logo to 15% of image width
        logo = Image.open(logo_path).convert("RGBA")
        target_width = int(img.width * 0.15)
        aspect_ratio = logo.height / logo.width
        target_height = int(target_width * aspect_ratio)
        logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Apply opacity (70%)
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.7))
        logo.putalpha(alpha)

        # Create watermark layer
        watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))

        # Position bottom-right with 20px margin
        position = (img.width - target_width - 20, img.height - target_height - 20)
        watermark_layer.paste(logo, position, logo)

        # Composite
        img = Image.alpha_composite(img, watermark_layer)

        # Convert back to RGB and save
        output = BytesIO()
        img.convert("RGB").save(output, format="PNG")
        return output.getvalue()

    except Exception as e:
        print(f"Watermark error: {e}")
        return image_data


def generate_prompts_with_gemini(
    category: str,
    product_name: str,
    image_analysis: str,
    aroma_data: Optional[Dict] = None,
    mode: str = "flash"
) -> Dict[str, str]:
    """Generate 10 prompts using Gemini."""

    model = "gemini-2.5-flash" if mode == "flash" else "gemini-2.5-pro"

    category_context = CATEGORY_RULES.get(category, {})
    category_rules = category_context.get("rules", [])

    aroma_context = ""
    if aroma_data:
        aroma_context = f"\nAroma: {aroma_data.get('name', '')}\nNotas: {', '.join(aroma_data.get('notas', []))}\nDescrição: {aroma_data.get('description', '')}"

    prompt = f"""
Você é um diretor de fotografia especializado em produtos de luxo e estética.

CATEGORIA: {category}
PRODUTO: {product_name}
ANÁLISE DA IMAGEM: {image_analysis}
{aroma_context}

REGRAS DA CATEGORIA:
{json.dumps(category_rules, ensure_ascii=False)}

{ANTI_CLICHE_DIRECTIVE}

TAREFA: Gere EXATAMENTE 10 prompts fotográficos únicos e criativos usando o PROMPT SYSTEM:
- hero_shot
- dark_moody
- ingredient_story
- lifestyle
- anti_cliche
- ambience
- close_up
- social_media
- smoke_aroma
- premium_context

CADA PROMPT DEVE:
1. Ser descritivo e detalhado (mínimo 150 caracteres)
2. Incluir especificidades técnicas (f-stop, iluminação, posição, ângulo)
3. Referenciar a análise da imagem fornecida
4. Evitar TOTALMENTE o Anti-Clichê
5. Para categoria velas: incorporar dados aromáticos
6. Para categoria home_spray: descrever mist e suspensão

Responda APENAS com JSON válido, neste formato exato:
{
    "hero_shot": "prompt completo aqui",
    "dark_moody": "prompt completo aqui",
    "ingredient_story": "prompt completo aqui",
    "lifestyle": "prompt completo aqui",
    "anti_cliche": "prompt completo aqui",
    "ambience": "prompt completo aqui",
    "close_up": "prompt completo aqui",
    "social_media": "prompt completo aqui",
    "smoke_aroma": "prompt completo aqui",
    "premium_context": "prompt completo aqui"
}
"""

    def call_gemini():
        client = gemini_client
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                max_output_tokens=4000,
            ),
        )
        return response.text

    try:
        result_text = retry_gemini_call(call_gemini)
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"Error generating prompts: {e}")

    # Fallback: use system templates
    return PROMPT_SYSTEM.copy()


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API status."""
    return {
        "app": "Chamaroma Studio API",
        "version": "1.0.0"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint with Gemini and aroma status."""
    aromas = get_all_aromas()
    return HealthResponse(
        status="healthy",
        gemini_configured=bool(GEMINI_API_KEY and genai),
        aroma_count=len(aromas),
        timestamp=datetime.now().isoformat()
    )


@app.get("/api/aromas", tags=["Aromas"])
async def list_aromas():
    """List all 17 aromas."""
    aromas = get_all_aromas()
    return {
        "aromas": [aroma.to_dict() if hasattr(aroma, 'to_dict') else aroma.__dict__ for aroma in aromas],
        "total": len(aromas)
    }


@app.get("/api/aromas/{aroma_id}", tags=["Aromas"])
async def get_aroma_detail(aroma_id: str):
    """Get single aroma detail."""
    aroma = get_aroma_by_id(aroma_id)
    if not aroma:
        raise HTTPException(status_code=404, detail="Aroma not found")
    return aroma.to_dict() if hasattr(aroma, 'to_dict') else aroma.__dict__


@app.get("/api/aromas/{aroma_id}/copy-ml", tags=["Copy"])
async def get_aroma_copy_ml(aroma_id: str):
    """ML-optimized copy for single aroma."""
    aroma = get_aroma_by_id(aroma_id)
    if not aroma:
        raise HTTPException(status_code=404, detail="Aroma not found")

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    prompt = f"""
Gere copy EXTREMAMENTE otimizado para ML (machine learning) e engagement máximo.

AROMA: {aroma.name if hasattr(aroma, 'name') else aroma.get('name')}
NOTAS: {aroma.notas if hasattr(aroma, 'notas') else aroma.get('notas')}
DESCRIÇÃO: {aroma.description if hasattr(aroma, 'description') else aroma.get('description')}

GERE:
1. headline_ml: 60 caracteres, máximo engagement, sem emoji
2. description_seo: 160 caracteres, keywords naturais
3. social_hook: 140 caracteres, parar em ponto de curiosidade
4. cta_conversion: 40 caracteres, ação direta
5. alt_text_image: 125 caracteres, descritivo para acessibilidade

Responda APENAS JSON:
{{
    "headline_ml": "...",
    "description_seo": "...",
    "social_hook": "...",
    "cta_conversion": "...",
    "alt_text_image": "..."
}}
"""

    def call_gemini():
        client = gemini_client
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=800),
        )
        return response.text

    try:
        result_text = retry_gemini_call(call_gemini)
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating copy: {str(e)}")


@app.get("/api/copy/batch", tags=["Copy"])
async def batch_copy():
    """Batch copy for all 17 aromas (for bot consumption)."""
    aromas = get_all_aromas()
    results = []

    for aroma in aromas:
        aroma_id = aroma.id if hasattr(aroma, 'id') else aroma.get('id')
        try:
            aroma_name = aroma.name if hasattr(aroma, 'name') else aroma.get('name')
            aroma_notas = aroma.notas if hasattr(aroma, 'notas') else aroma.get('notas')
            aroma_desc = aroma.description if hasattr(aroma, 'description') else aroma.get('description')

            prompt = f"""Gere copy otimizado para {aroma_name}.
Notas: {aroma_notas}
Descrição: {aroma_desc}

Responda JSON com: headline_ml, description_seo, social_hook, cta_conversion, alt_text_image"""

            if genai and GEMINI_API_KEY:
                def call_gemini():
                    client = gemini_client
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=600),
                    )
                    return response.text

                result_text = retry_gemini_call(call_gemini)
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    copy_data = json.loads(json_match.group())
                    results.append({
                        "aroma_id": aroma_id,
                        "aroma_name": aroma_name,
                        "copy": copy_data
                    })
        except Exception as e:
            print(f"Error generating copy for {aroma_id}: {e}")

    return {"aromas": results, "total": len(results)}


@app.post("/api/generate", response_model=GeneratedPrompts, tags=["Generation"])
async def generate_prompts(request: GeneratePromptsRequest):
    """Generate 10 prompts from image analysis."""

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    # Extract base64 if it's a data URL
    image_url = request.image_url
    if image_url.startswith("data:"):
        image_data = base64.b64decode(extract_base64_from_data_url(image_url))
    elif image_url.startswith("http"):
        import urllib.request
        try:
            image_data = urllib.request.urlopen(image_url).read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image URL: {str(e)}")
    else:
        # Assume it's base64
        try:
            image_data = base64.b64decode(image_url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    # Analyze image with Gemini
    def analyze_image():
        client = gemini_client

        # Upload image file first
        response = client.files.upload(
            file=types.File(
                mime_type="image/jpeg",
                data=image_data
            )
        )

        file_uri = response.uri

        # Analyze
        analysis_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                f"Analise esta imagem de {request.name_size} para fotografia de produto ({request.category}). Descreva: composição, iluminação, textura, cores dominantes, materiais visíveis, contexto. Seja técnico e específico.",
                types.Part.from_uri(file_uri, mime_type="image/jpeg")
            ],
            config=types.GenerateContentConfig(temperature=0.5, max_output_tokens=800),
        )

        return analysis_response.text

    try:
        image_analysis = retry_gemini_call(analyze_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

    # Get aroma data if provided
    aroma_data = None
    if request.aroma:
        aroma = get_aroma_by_id(request.aroma)
        if aroma:
            aroma_data = aroma.to_dict() if hasattr(aroma, 'to_dict') else aroma.__dict__

    # Generate prompts
    prompts = generate_prompts_with_gemini(
        category=request.category,
        product_name=request.name_size,
        image_analysis=image_analysis,
        aroma_data=aroma_data,
        mode=request.mode
    )

    return GeneratedPrompts(
        category=request.category,
        product_name=request.name_size,
        prompts=prompts,
        aroma_data=aroma_data
    )


@app.post("/api/generate-image", response_model=GenerateImageResponse, tags=["Generation"])
async def generate_image(request: GenerateImageRequest):
    """Generate image using Imagen."""

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    model = "imagen-4.0-fast-generate-001" if request.model == "flash" else "nano-banana-pro-preview"

    # Add anti-cliche directive to prompt
    full_prompt = f"{request.prompt}\n\n{ANTI_CLICHE_DIRECTIVE}"

    def generate():
        client = gemini_client
        response = client.models.generate_images(
            model=model,
            prompt=full_prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio=request.aspect_ratio,
                safety_filter_level="block_only_high",
                number_of_images=1,
            ),
        )
        return response

    try:
        result = retry_gemini_call(generate)

        if not result.generated_images or len(result.generated_images) == 0:
            raise HTTPException(status_code=500, detail="No image generated")

        image_data = result.generated_images[0].image.data

        # Add watermark if specified
        if request.watermark:
            image_data = add_watermark_to_image(image_data, request.watermark)

        image_base64 = base64.b64encode(image_data).decode('utf-8')

        return GenerateImageResponse(
            image_base64=image_base64,
            model=request.model,
            aspect_ratio=request.aspect_ratio
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@app.post("/api/generate-video-scripts", response_model=VideoScriptsResponse, tags=["Video"])
async def generate_video_scripts(request: VideoScriptsRequest):
    """Generate video scripts for YouTube, Instagram Feed, and Stories."""

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    model = "gemini-2.5-flash" if request.mode == "flash" else "gemini-2.5-pro"

    prompt = f"""
Crie roteiros de vídeo para {request.product_name} ({request.category}) da marca {request.product_brand}.
Uso: {request.content_for}
Imagens selecionadas: {', '.join(request.selected_images)}

GERE 3 FORMATOS:

1. CLIPS ML (YouTube Shorts, TikTok):
   - 3-5 clips de 15-30 segundos
   - Hook nos primeiros 2 segundos
   - Texto em movimento
   - CTA claro

2. INSTAGRAM FEED:
   - 3-4 carrosséis temáticos
   - 5-7 slides por carrossel
   - Copy envolvente
   - Hashtags estratégicas

3. INSTAGRAM STORIES:
   - 8-10 stories com fluxo narrativo
   - Textos curtos e diretos
   - Stickers/interação
   - CTA em story final

Responda JSON com: clips_ml (array), instagram_feed (array), instagram_stories (array)
"""

    def call_gemini():
        client = gemini_client
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.8, max_output_tokens=3000),
        )
        return response.text

    try:
        result_text = retry_gemini_call(call_gemini)
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return VideoScriptsResponse(
                clips_ml=data.get("clips_ml", []),
                instagram_feed=data.get("instagram_feed", []),
                instagram_stories=data.get("instagram_stories", [])
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")


@app.post("/api/generate-video-narration", response_model=VideoNarrationResponse, tags=["Video"])
async def generate_video_narration(request: VideoNarrationRequest):
    """Generate video narration/voiceover script."""

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    model = "gemini-2.5-flash" if request.mode == "flash" else "gemini-2.5-pro"

    prompt = f"""
Crie narrativa de vídeo premium para {request.product_name} ({request.category}).
Marca: {request.product_brand}
Plataforma: {request.content_for}

IMAGENS/CENAS:
- Hero Shot: {request.hero_shot}
- Lifestyle: {request.lifestyle}
- Dark Moody: {request.dark_moody}
- Smoke/Aroma: {request.smoke_aroma}

{ANTI_CLICHE_DIRECTIVE}

CRIE:
1. Narração para vídeo principal (90-120 segundos)
2. Estrutura: abertura cinematográfica > apresentação produto > story/benefit > CTA
3. Tom: premium, editorial, inspirador, SEM clichê
4. Ritmo: alterna descrições visuais com copy persuasivo
5. Marca presença em transições

Responda APENAS com a narração em português, sem marcações, com linha breaks claros entre seções.
"""

    def call_gemini():
        client = gemini_client
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.8, max_output_tokens=1500),
        )
        return response.text

    try:
        narracao = retry_gemini_call(call_gemini)
        return VideoNarrationResponse(narracao=narracao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narration generation failed: {str(e)}")


@app.post("/api/generate-instagram-post", response_model=InstagramPostResponse, tags=["Social"])
async def generate_instagram_post(request: InstagramPostRequest):
    """Generate optimized Instagram post with copy, hashtags, and carousel."""

    if not genai or not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini not configured")

    model = "gemini-2.5-flash" if request.mode == "flash" else "gemini-2.5-pro"

    prompts_context = json.dumps(request.prompts) if request.prompts else "Prompts disponíveis na plataforma"
    images_context = ", ".join(request.generated_image_keys) if request.generated_image_keys else "Imagens geradas"

    prompt = f"""
Crie post Instagram perfeito para {request.product_name} ({request.category}) - {request.product_brand}.

{ANTI_CLICHE_DIRECTIVE}

CONTEXTO:
- Prompts: {prompts_context}
- Imagens: {images_context}

GERE (JSON):
1. post_type: "carousel" ou "single"
2. caption: 150-200 caracteres, hook + benefit + CTA
3. hashtags: array 15-20 tags relevantes (sem #)
4. slides: array com ordem das imagens/textos
5. best_posting_time: horário recomendado (HH:MM)
6. content_pillar: "educacional", "inspiração", "produto", "lifestyle", etc
7. cta_type: "comprar", "saiba-mais", "descubra", "reserve"
8. alt_text: descrição acessível 100-125 caracteres

Responda APENAS JSON válido.
"""

    def call_gemini():
        client = gemini_client
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.8, max_output_tokens=2000),
        )
        return response.text

    try:
        result_text = retry_gemini_call(call_gemini)
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return InstagramPostResponse(
                post_type=data.get("post_type", "carousel"),
                caption=data.get("caption", ""),
                hashtags=data.get("hashtags", []),
                slides=data.get("slides", []),
                best_posting_time=data.get("best_posting_time", "09:00"),
                content_pillar=data.get("content_pillar", "produto"),
                cta_type=data.get("cta_type", "saiba-mais"),
                alt_text=data.get("alt_text", "")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Instagram post generation failed: {str(e)}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc), "timestamp": datetime.now().isoformat()}
    )


# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    aromas = get_all_aromas()
    print(f"✓ Chamaroma Studio API initialized")
    print(f"✓ Gemini configured: {bool(GEMINI_API_KEY and genai)}")
    print(f"✓ Aromas loaded: {len(aromas)}")
    print(f"✓ CORS origins: {len(ALLOWED_ORIGINS)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("✓ Chamaroma Studio API shutdown")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
