from pydantic import BaseModel, Field
from typing import Optional


class PiramideOlfativa(BaseModel):
    saida: list[str]
    corpo: list[str]
    fundo: list[str]


class CopyRaioX(BaseModel):
    titulo_seo_ml: str = Field(..., max_length=60)
    bullets_matadores: list[str] = Field(..., min_items=5, max_items=5)
    gancho_emocional: str
    descricao_sensorial: str
    cta_fechamento: str


class MockupVisual(BaseModel):
    cor_cera: str
    hex_cera: str
    gradiente_secundario: Optional[str] = None


class Aroma(BaseModel):
    id: str
    nome: str
    emoji: str
    categoria: str
    descricao: str
    notas_sensoriais: list[str]
    mood: list[str]
    ocasioes: list[str]
    piramide: PiramideOlfativa
    copy_raio_x: CopyRaioX
    mockup: MockupVisual


CATALOGO_AROMAS = [
    # FRESCOS
    Aroma(
        id="limao-siciliano",
        nome="Limão Siciliano",
        emoji="🍋",
        categoria="frescos",
        descricao="Um aroma cítrico radiante que captura a essência do Mediterrâneo. Limão Siciliano traz vivacidade e frescor refrescante, perfeito para despertar os sentidos.",
        notas_sensoriais=["Cítrico vibrante", "Fresco", "Brilhante", "Harmonioso", "Energético"],
        mood=["Energizado", "Feliz", "Revigorado"],
        ocasioes=["Manhã", "Trabalho", "Primavera"],
        piramide=PiramideOlfativa(
            saida=["Limão Siciliano", "Verbena"],
            corpo=["Folha de Limão", "Neroli"],
            fundo=["Almíscar Branco", "Cedro"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Limão Siciliano 240ml Cera Vegetal",
            bullets_matadores=[
                "✨ Aroma cítrico fresco com Limão Siciliano e Verbena",
                "🌱 Feito com cera vegetal sustentável e pavio de madeira",
                "⏱️ Queima por até 40 horas de aromatização contínua",
                "🎁 Perfeito para presentear ou aromatizar sua casa",
                "💚 Fragrância que energiza e traz bem-estar ao ambiente"
            ],
            gancho_emocional="Acorde seus sentidos com a vitalidade do Mediterrâneo",
            descricao_sensorial="Experimente a explosão de frescor do Limão Siciliano. Suas notas cítricas vibrantes se desdobram em folhas de limão delicadas e neroli sofisticado, apoiadas por almíscar branco e cedro ao fundo, criando um aroma que perdura e revitaliza.",
            cta_fechamento="Transforme seu espaço em um oásis de frescor. Compre agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Amarelo Claro",
            hex_cera="#F5E050"
        )
    ),
    Aroma(
        id="limonilha",
        nome="Limonilha",
        emoji="🍈",
        categoria="frescos",
        descricao="Uma combinação suave entre lima e limão que traz leveza e frescor tropical. Limonilha é perfeita para momentos que pedem revitalização gentil.",
        notas_sensoriais=["Tropical", "Leve", "Herbal", "Refrescante", "Suave"],
        mood=["Relaxado", "Leve", "Tranquilo"],
        ocasioes=["Tarde", "Leitura", "Verão"],
        piramide=PiramideOlfativa(
            saida=["Lima", "Limão"],
            corpo=["Hortelã", "Manjericão"],
            fundo=["Vetiver", "Musk"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Limonilha 240ml Cera Vegetal Artesanal",
            bullets_matadores=[
                "🌿 Aroma tropical com Lima, Limão, Hortelã e Manjericão",
                "🍃 Blend herbal refrescante que acalma e revitaliza",
                "🌍 Cera 100% vegetal com queima limpa e longa duração",
                "🏡 Ideal para salas de estar, quartos e áreas de trabalho",
                "💨 Aroma sutil que não compete com outros perfumes"
            ],
            gancho_emocional="Encontre leveza e tranquilidade em cada queimada",
            descricao_sensorial="Limonilha convida você a um passeio tropical. Lima e limão se abraçam delicadamente enquanto hortelã e manjericão adicionam uma camada herbal refrescante. Vetiver e musk no fundo criam uma base duradoura que eleva o aroma a um nível de sofisticação rara.",
            cta_fechamento="Leve a leveza tropical para sua casa. Peça agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Verde Claro",
            hex_cera="#C5E384"
        )
    ),
    Aroma(
        id="blueberry",
        nome="Blueberry",
        emoji="🫐",
        categoria="frescos",
        descricao="Um aroma frutado que celebra a doçura do mirtilo e a elegância da violeta. Blueberry combina frescor com sofisticação em uma experiência olfativa única.",
        notas_sensoriais=["Frutado", "Floral", "Sofisticado", "Misterioso", "Suculento"],
        mood=["Refinado", "Confortável", "Sedutor"],
        ocasioes=["Noite", "Jantar", "Outono"],
        piramide=PiramideOlfativa(
            saida=["Mirtilo", "Cassis"],
            corpo=["Violeta", "Íris"],
            fundo=["Baunilha", "Sândalo"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Blueberry 240ml Vegetal Premium",
            bullets_matadores=[
                "🫐 Aroma gourmet com Mirtilo, Cassis, Violeta e Íris",
                "✨ Sofisticação floral que cativa desde o primeiro aroma",
                "🕯️ Queima uniforme com até 40 horas de duração",
                "🎭 Traz toque de elegância para qualquer ambiente",
                "💜 Aroma que evolui ao longo da queimada, revelando camadas"
            ],
            gancho_emocional="Mergulhe em um aroma sofisticado que sussurra elegância",
            descricao_sensorial="Blueberry é um convite à sofisticação. O aroma inicial traz mirtilo e cassis suculentos, evoluindo para violeta delicada e íris refinada. Conforme queima, revela notas de baunilha cremosa e sândalo envolvente, criando uma experiência sensorial em camadas.",
            cta_fechamento="Eleve seu espaço com elegância frutal. Adquira já!"
        ),
        mockup=MockupVisual(
            cor_cera="Roxo Escuro",
            hex_cera="#4A3B8F"
        )
    ),
    Aroma(
        id="energia-do-mar",
        nome="Energia do Mar",
        emoji="🌊",
        categoria="frescos",
        descricao="Uma essência oceânica que captura o poder e a liberdade do mar. Energia do Mar combina ozônio, algas marinhas e madeira flutuante em uma ode ao elemento água.",
        notas_sensoriais=["Marítimo", "Salgado", "Ozônico", "Crisp", "Revitalizante"],
        mood=["Energizado", "Livre", "Aventureiro"],
        ocasioes=["Dia inteiro", "Praia", "Escapada"],
        piramide=PiramideOlfativa(
            saida=["Ozônio", "Bergamota"],
            corpo=["Algas", "Sal Marinho"],
            fundo=["Âmbar", "Madeira Flutuante"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Energia do Mar 240ml Cera Vegetal",
            bullets_matadores=[
                "🌊 Aroma marítimo com Ozônio, Bergamota, Algas e Sal Marinho",
                "🏄 Traz a energia oceânica para dentro de sua casa",
                "🌬️ Frescor crisp que purifica e revitaliza o ambiente",
                "⚓ Perfeito para amantes da natureza e do mar",
                "💙 Aromaterapeuta recomenda para ânimo e vitalidade"
            ],
            gancho_emocional="Sinta a liberdade e o poder do oceano a cada respiro",
            descricao_sensorial="Energia do Mar traz o oceano para você. Ozônio e bergamota criam uma saída aérea que evoca a brisa marítima. Algas e sal marinho adicionam uma camada orgânica e autêntica, enquanto âmbar e madeira flutuante criam uma base que lembra madeira seca pela ação das ondas.",
            cta_fechamento="Leve a energia do mar para seu refúgio. Compre agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Azul Oceano",
            hex_cera="#2E86AB"
        )
    ),
    Aroma(
        id="flor-de-laranjeira",
        nome="Flor de Laranjeira",
        emoji="🌼",
        categoria="frescos",
        descricao="Uma celebração delicada da flor de laranjeira com néroli e bergamota. Este aroma clássico traz frescor botânico e elegância atemporal.",
        notas_sensoriais=["Floral", "Cítrico", "Clássico", "Luminoso", "Aromático"],
        mood=["Sereno", "Equilibrado", "Gracioso"],
        ocasioes=["Qualquer momento", "Meditação", "Dias especiais"],
        piramide=PiramideOlfativa(
            saida=["Néroli", "Bergamota"],
            corpo=["Flor de Laranjeira", "Jasmim"],
            fundo=["Musk Branco", "Cedro"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Flor de Laranjeira 240ml Vegetal",
            bullets_matadores=[
                "🌸 Aroma clássico com Néroli, Bergamota e Flor de Laranjeira",
                "💐 Elegância floral que traz paz e serenidade",
                "🕯️ Queima lenta e uniforme com cera 100% natural",
                "✨ Aroma versátil perfeito para qualquer ambiente",
                "🍊 Fragrância tradicional que agrada gerações"
            ],
            gancho_emocional="Encontre serenidade na beleza clássica da flor de laranja",
            descricao_sensorial="Flor de Laranjeira é um passeio botânico. Néroli e bergamota abrem com frescor luminoso, a flor de laranjeira desabrocha no coração acompanhada por jasmim suave, enquanto musk branco e cedro criam uma base elegante e duradoura que envolve o ambiente com graça.",
            cta_fechamento="Traga elegância atemporal para seu lar. Encomende agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Amarelo Dourado",
            hex_cera="#FFB347"
        )
    ),
    # FLORAIS
    Aroma(
        id="lavanda",
        nome="Lavanda",
        emoji="💜",
        categoria="florais",
        descricao="A essência calmante da lavanda encontra eucalipto fresco e ervas tranquilizantes. Um clássico que traz paz e relaxamento para qualquer espaço.",
        notas_sensoriais=["Herbal", "Floral", "Calmante", "Puro", "Repousante"],
        mood=["Tranquilo", "Meditativo", "Restaurador"],
        ocasioes=["Noite", "Sono", "Spa"],
        piramide=PiramideOlfativa(
            saida=["Lavanda", "Eucalipto"],
            corpo=["Gerânio", "Alecrim"],
            fundo=["Tonka", "Musgo de Carvalho"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Lavanda 240ml Cera Natural Relaxante",
            bullets_matadores=[
                "💜 Aroma clássico de Lavanda pura com Eucalipto e Alecrim",
                "😴 Ideal para quarto, banheiro e espaços de descanso",
                "🧘 Ajuda a criar ambiente relaxante para meditação e yoga",
                "🌿 Aromaterapia natural para redução de estresse",
                "✨ Fragrância suave que não agride os sentidos"
            ],
            gancho_emocional="Escape do caos e mergulhe em tranquilidade pura",
            descricao_sensorial="Lavanda envolve você em paz. A flor delicada se abre com eucalipto fresco e alecrim aromático, enquanto gerânio adiciona uma dimensão floral sofisticada. Tonka e musgo de carvalho ao fundo criam uma base quente e confortável que convida ao descanso.",
            cta_fechamento="Prepare seu refúgio de calma. Peça sua Lavanda agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Roxo Macio",
            hex_cera="#9B72AA"
        )
    ),
    Aroma(
        id="orquidea",
        nome="Orquídea",
        emoji="🌺",
        categoria="florais",
        descricao="Uma celebração de exoticidade e sensualidade. Orquídea mistura peônia, lírio e orquídea verdadeira em uma composição floral sofisticada e envolvente.",
        notas_sensoriais=["Floral", "Sensual", "Exótico", "Refinado", "Misterioso"],
        mood=["Sofisticado", "Sedutor", "Feminino"],
        ocasioes=["Noite", "Encontro", "Celebração"],
        piramide=PiramideOlfativa(
            saida=["Peônia", "Lírio"],
            corpo=["Orquídea", "Rosa"],
            fundo=["Sândalo", "Almíscar"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Orquídea 240ml Premium Vegetal",
            bullets_matadores=[
                "🌺 Aroma floral exótico com Peônia, Lírio, Orquídea e Rosa",
                "✨ Sofisticação que impressiona e cativa de imediato",
                "💐 Fragrância sensual perfeita para momentos especiais",
                "🌸 Base duradoura que perdura por horas",
                "💎 Aroma premium que eleva qualquer ambiente"
            ],
            gancho_emocional="Descubra o lado sensual e sofisticado de você mesma",
            descricao_sensorial="Orquídea é pura sofisticação. Peônia e lírio se abrem em harmonia, enquanto a orquídea verdadeira traz exoticidade e rosa adiciona feminilidade. Sândalo cremoso e almíscar misterioso ao fundo criam um aroma que envolve, seduz e permanece na memória.",
            cta_fechamento="Celebre sua sofisticação. Adquira Orquídea agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Magenta Suave",
            hex_cera="#DA70D6"
        )
    ),
    # DOCES
    Aroma(
        id="baunilha",
        nome="Baunilha",
        emoji="🍦",
        categoria="doces",
        descricao="Doçura pura e reconfortante. Baunilha traz o calor cremoso da baunilha autêntica, caramelo e canela para momentos de conforto absoluto.",
        notas_sensoriais=["Doce", "Cremoso", "Aquecedor", "Confortável", "Nostálgico"],
        mood=["Aconchegante", "Feliz", "Reconfortado"],
        ocasioes=["Noite", "Inverno", "Repouso"],
        piramide=PiramideOlfativa(
            saida=["Baunilha", "Caramelo"],
            corpo=["Leite Condensado", "Canela"],
            fundo=["Benjoim", "Tonka"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Baunilha 240ml Doce Cera Vegetal",
            bullets_matadores=[
                "🍦 Aroma doce confortável com Baunilha pura e Caramelo",
                "🏠 Perfeito para criar ambiente aconchegante e acolhedor",
                "🕯️ Queima longa que mantém o aroma por horas",
                "❤️ Reconfortante natural que aquece e envolve",
                "🎁 Ideal para presentear quem ama aromas doces"
            ],
            gancho_emocional="Sinta o abraço caloroso da baunilha verdadeira",
            descricao_sensorial="Baunilha envolve você em conforto. O aroma puro de baunilha se abre com caramelo dourado, enquanto leite condensado adicionada uma doçura cremosa e canela traz calor especiado. Benjoim e tonka ao fundo criam uma base que abraça e permanece, como um abraço quente.",
            cta_fechamento="Traga aconchego para sua casa. Compre sua Baunilha!"
        ),
        mockup=MockupVisual(
            cor_cera="Bege Cálido",
            hex_cera="#F3E5AB"
        )
    ),
    Aroma(
        id="cookies",
        nome="Cookies",
        emoji="🍪",
        categoria="doces",
        descricao="Um aroma gourmand que traz à mente biscoitos caseiros ainda quentes. Cookies combina baunilha, manteiga e chocolate em uma delícia olfativa.",
        notas_sensoriais=["Gourmand", "Quente", "Delicioso", "Nostálgico", "Aconchegante"],
        mood=["Feliz", "Descontraído", "Guloso"],
        ocasioes=["Tarde", "Café da tarde", "Qualquer hora"],
        piramide=PiramideOlfativa(
            saida=["Baunilha", "Manteiga"],
            corpo=["Chocolate", "Canela"],
            fundo=["Caramelo", "Tonka"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Cookies 240ml Gourmand Cera Natural",
            bullets_matadores=[
                "🍪 Aroma gourmand com Baunilha, Chocolate, Canela perfeito",
                "😋 Traz a sensação de biscoitos caseiros quentinhos",
                "👨‍🍳 Fragrância que evoca memória afetiva de conforto",
                "☕ Combinação perfeita para ambiente de café da tarde",
                "💛 Aroma que transmite aconchego e felicidade instantânea"
            ],
            gancho_emocional="Volte à memória afetiva de biscoitos caseiros quentinhos",
            descricao_sensorial="Cookies é puro conforto. Baunilha e manteiga se abrem cremosas, chocolate aparece trazendo profundidade gourmand, enquanto canela aquece o aroma. Caramelo e tonka ao fundo criam uma base doce que lembra biscoitos ainda no forno, quentes e reconfortantes.",
            cta_fechamento="Leve conforto gourmand para sua casa. Peça agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Marrom Biscoito",
            hex_cera="#D2691E"
        )
    ),
    Aroma(
        id="marshmallow",
        nome="Marshmallow",
        emoji="🩷",
        categoria="doces",
        descricao="Doçura aérea e delicada que evoca algodão doce e marshmallow fresco. Um aroma leve, feminino e envolvente para quem ama doces sofisticados.",
        notas_sensoriais=["Aérea", "Adocicada", "Macia", "Infantil", "Delicada"],
        mood=["Ingênuo", "Dócil", "Encantado"],
        ocasioes=["Dia", "Primavera", "Celebração"],
        piramide=PiramideOlfativa(
            saida=["Açúcar", "Baunilha"],
            corpo=["Marshmallow", "Creme"],
            fundo=["Musk", "Algodão Doce"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Marshmallow 240ml Rosa Cera Vegetal",
            bullets_matadores=[
                "🩷 Aroma adocicado leve com Marshmallow e Algodão Doce",
                "☁️ Fragrância aérea que flutua delicadamente no ar",
                "💕 Perfeito para quarto de menina ou espaço feminino",
                "🎀 Aroma que traz leveza e ternura ao ambiente",
                "✨ Ideal para quem prefere aromas suaves e agradáveis"
            ],
            gancho_emocional="Flutue em doçura pura e delicada como uma nuvem",
            descricao_sensorial="Marshmallow é leveza em essência. Açúcar e baunilha abrem delicadamente, marshmallow e creme adicionam uma textura aérea, enquanto algodão doce e musk criam uma base que flutua no ar como nuvem perfumada, deixando uma sensação de maciez e ternura.",
            cta_fechamento="Leve leveza doce para seu espaço. Adquira agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Rosa Pastel",
            hex_cera="#FFB6C1"
        )
    ),
    Aroma(
        id="chale",
        nome="Chalé",
        emoji="🏔️",
        categoria="doces",
        descricao="Aquecimento especiado que evoca uma noite em chalé de montanha. Chalé mistura pinho, canela e madeira defumada em conforto rústico e elegante.",
        notas_sensoriais=["Especiado", "Quente", "Rústico", "Amadeirado", "Defumado"],
        mood=["Aconchegante", "Nostálgico", "Refinado"],
        ocasioes=["Noite", "Inverno", "Encontro"],
        piramide=PiramideOlfativa(
            saida=["Pinho", "Eucalipto"],
            corpo=["Canela", "Cravo"],
            fundo=["Madeira Defumada", "Âmbar"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Chalé 240ml Rústico Cera Natural",
            bullets_matadores=[
                "🏔️ Aroma especiado com Pinho, Canela, Cravo e Madeira Defumada",
                "🔥 Traz sensação de aquecimento e aconchego de chalé",
                "❄️ Perfeito para criar ambiente cozy durante o inverno",
                "🪵 Fragrância rústica e elegante que impressiona",
                "🌲 Ideal para salas de estar e ambientes sofisticados"
            ],
            gancho_emocional="Sinta o calor de uma lareira em noite de montanha",
            descricao_sensorial="Chalé envolve em rústico aconchego. Pinho e eucalipto abrem com frescor verde, canela e cravo trazem especiarias aquecedoras, enquanto madeira defumada e âmbar criam uma base profunda que evoca lareira quente, conforto rústico e elegância sofisticada.",
            cta_fechamento="Traga a magia do chalé para seu lar. Compre agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Marrom Escuro",
            hex_cera="#8B4513"
        )
    ),
    Aroma(
        id="noite-de-melao",
        nome="Noite de Melão",
        emoji="🍈",
        categoria="doces",
        descricao="Frescor frutal encontra sofisticação floral. Noite de Melão combina melão suculento com pêssego, flor de lótus e lírio em aroma envolvente e refrescante.",
        notas_sensoriais=["Frutal", "Floral", "Suculento", "Leve", "Refinado"],
        mood=["Refrescado", "Equilibrado", "Sofisticado"],
        ocasioes=["Verão", "Festa", "Celebração"],
        piramide=PiramideOlfativa(
            saida=["Melão", "Pêssego"],
            corpo=["Flor de Lótus", "Lírio"],
            fundo=["Musk", "Cedro Branco"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Noite de Melão 240ml Frutal Vegetal",
            bullets_matadores=[
                "🍈 Aroma frutal sofisticado com Melão, Pêssego e Flor Lótus",
                "🌸 Fragrância refrescante que combina fruta com flor perfeita",
                "☀️ Ideal para verão e festas ao ar livre",
                "💚 Equilibrio entre frescor e sofisticação floral",
                "✨ Aroma que transmite leveza e bem-estar"
            ],
            gancho_emocional="Celebre a noite com frescor frutal sofisticado",
            descricao_sensorial="Noite de Melão é refrescante sofisticado. Melão suculento e pêssego abrem com maciez frutal, flor de lótus e lírio adicionam sofisticação floral delicada, enquanto musk e cedro branco criam uma base que perdura, equilibrando frescor com elegância.",
            cta_fechamento="Leve sofisticação frutal para sua casa. Peça agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Verde Claro",
            hex_cera="#98FB98"
        )
    ),
    # ESPECIAIS
    Aroma(
        id="alecrim",
        nome="Alecrim",
        emoji="🌿",
        categoria="especiais",
        descricao="Erva aromática pura que combina alecrim, limão e lavanda para um aroma revitalizante. Alecrim traz foco mental e energia equilibrada.",
        notas_sensoriais=["Herbal", "Cítrico", "Revigorador", "Claro", "Natural"],
        mood=["Focado", "Energizado", "Alerta"],
        ocasioes=["Manhã", "Trabalho", "Estudo"],
        piramide=PiramideOlfativa(
            saida=["Alecrim", "Limão"],
            corpo=["Lavanda", "Sálvia"],
            fundo=["Cedro", "Patchouli"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Alecrim 240ml Herbal Cera Vegetal",
            bullets_matadores=[
                "🌿 Aroma herbal puro com Alecrim, Limão, Lavanda e Sálvia",
                "🧠 Favorece concentração e clareza mental naturalmente",
                "⚡ Energia revigoradora que aumenta disposição",
                "🏢 Perfeito para home office e áreas de trabalho",
                "🌱 100% natural com propriedades aromaterápicas comprovadas"
            ],
            gancho_emocional="Ative seu potencial com clareza mental e foco total",
            descricao_sensorial="Alecrim traz clareza em vapor. Alecrim puro e limão abrem refrescantes, lavanda e sálvia adicionam sofisticação herbal, cedro e patchouli criam uma base que enraíza e estabiliza. Um aroma que sharpens mente e eleva disposição.",
            cta_fechamento="Potencialize seu foco. Compre Alecrim agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Verde Escuro",
            hex_cera="#2E8B57"
        )
    ),
    Aroma(
        id="amora",
        nome="Amora",
        emoji="🫐",
        categoria="especiais",
        descricao="Frutas vermelhas vibrantes encontram sofisticação floral. Amora celebra amora e framboesa com rosa e peônia em aroma frutado e sensual.",
        notas_sensoriais=["Frutal", "Floral", "Sensual", "Profundo", "Elegante"],
        mood=["Sedutora", "Glamourosa", "Sofisticada"],
        ocasioes=["Noite", "Celebração", "Encontro"],
        piramide=PiramideOlfativa(
            saida=["Amora", "Framboesa"],
            corpo=["Rosa", "Peônia"],
            fundo=["Musk", "Baunilha"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Amora 240ml Frutal Vegetal Premium",
            bullets_matadores=[
                "🫐 Aroma sensual com Amora, Framboesa, Rosa e Peônia",
                "💜 Frutas vermelhas que encontram sofisticação floral perfeita",
                "✨ Fragrância profunda que deixa marca de elegância",
                "💋 Perfeito para criar atmosfera de sofisticação sensual",
                "🌹 Aroma que evolui ao longo da noite, revelando camadas"
            ],
            gancho_emocional="Desperte seu lado sofisticado e sensualmente elegante",
            descricao_sensorial="Amora é frutal sedutor. Amora e framboesa abrem vibrantes e suculentas, rosa e peônia florescem adicionando sofisticação floral, musk e baunilha ao fundo criam uma base sensual e duradoura que permanece na pele e na memória.",
            cta_fechamento="Eleve sua sofisticação sensual. Adquira Amora agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Roxo Escuro",
            hex_cera="#8B008B"
        )
    ),
    Aroma(
        id="bamboo",
        nome="Bamboo",
        emoji="🎋",
        categoria="especiais",
        descricao="Frescor oriental que celebra bambu e chá verde. Bamboo traz leveza zen e tranquilidade verdadeira para momentos de meditação.",
        notas_sensoriais=["Fresco", "Zen", "Oriental", "Herbáceo", "Limpo"],
        mood=["Meditativo", "Tranquilo", "Equilibrado"],
        ocasioes=["Meditação", "Yoga", "Spa"],
        piramide=PiramideOlfativa(
            saida=["Bambu", "Chá Verde"],
            corpo=["Jasmim", "Folhas Verdes"],
            fundo=["Musgo", "Vetiver"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Bamboo 240ml Zen Cera Vegetal",
            bullets_matadores=[
                "🎋 Aroma oriental zen com Bambu, Chá Verde e Jasmim",
                "🧘 Favorece meditação, yoga e práticas contemplativas",
                "☘️ Frescor oriental que traz tranquilidade verdadeira",
                "🌿 Fragrância limpa que purifica e harmoniza espaço",
                "💚 Ideal para criar santuário pessoal de paz interior"
            ],
            gancho_emocional="Encontre equilíbrio zen em cada respiração aromática",
            descricao_sensorial="Bamboo traz serenidade oriental. Bambu e chá verde abrem fresco e herbáceo, jasmim e folhas verdes adicionam leveza e pureza, musgo e vetiver criam uma base que enraíza e estabiliza. Um aroma que convida à meditação profunda e paz interior.",
            cta_fechamento="Cultive sua paz interior. Compre Bamboo agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Verde Fluorescente",
            hex_cera="#7CFC00"
        )
    ),
    Aroma(
        id="bambomalloow",
        nome="Bambomaloow",
        emoji="🎀",
        categoria="especiais",
        descricao="Uma fusão criativa entre bambu zen e marshmallow doce. Bambomalloow equilibra frescor oriental com doçura aérea em aroma único e cativante.",
        notas_sensoriais=["Fresco-Doce", "Delicado", "Único", "Equilibrado", "Encantador"],
        mood=["Criativo", "Leve", "Sofisticado"],
        ocasioes=["Tarde", "Criatividade", "Qualquer hora"],
        piramide=PiramideOlfativa(
            saida=["Bambu", "Baunilha"],
            corpo=["Marshmallow", "Flor de Cerejeira"],
            fundo=["Musk", "Sândalo"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Bambomalloow 240ml Criativo Vegetal",
            bullets_matadores=[
                "🎀 Aroma criativo único que mescla Bambu com Marshmallow",
                "✨ Equilibrio perfeito entre frescor oriental e doçura leve",
                "🎨 Fragrância que inspira criatividade e imaginação",
                "💕 Perfeito para ambiente de trabalho criativo ou quarto",
                "🌸 Aroma sofisticado que surpreende e encanta"
            ],
            gancho_emocional="Desperte sua criatividade com frescor doce único",
            descricao_sensorial="Bambomalloow é criatividade em aroma. Bambu fresco encontra baunilha delicada, marshmallow e flor de cerejeira adicionam doçura sofisticada, musk e sândalo criam uma base que equilibra frescor com maciez. Um aroma que inspira imaginação e auto-expressão.",
            cta_fechamento="Liberte sua criatividade. Peça Bambomalloow agora!"
        ),
        mockup=MockupVisual(
            cor_cera="Rosa Suave",
            hex_cera="#FFB6C1"
        )
    ),
    Aroma(
        id="sublime-blanc",
        nome="Sublime Blanc",
        emoji="🤍",
        categoria="especiais",
        descricao="Elegância branca pura que celebra sofisticação e pureza. Sublime Blanc mistura bergamota, pera, jasmim e flor de laranjeira em aroma transcendente.",
        notas_sensoriais=["Sofisticado", "Puro", "Luminoso", "Elegante", "Transcendente"],
        mood=["Elegante", "Sereno", "Divino"],
        ocasioes=["Ocasião especial", "Cerimônia", "Noite"],
        piramide=PiramideOlfativa(
            saida=["Bergamota", "Pera"],
            corpo=["Jasmim", "Flor de Laranjeira"],
            fundo=["Almíscar", "Cedro Branco"]
        ),
        copy_raio_x=CopyRaioX(
            titulo_seo_ml="Vela Aromática Sublime Blanc 240ml Premium Vegetal",
            bullets_matadores=[
                "🤍 Aroma premium com Bergamota, Pera, Jasmim transcendente",
                "✨ Elegância branca pura que traz sofisticação máxima",
                "💎 Fragrância de ocasião que marca presença com graça",
                "🌺 Perfeito para celebrar momentos especiais memoráveis",
                "👑 Aroma que transmite poder, graça e transcendência"
            ],
            gancho_emocional="Alcance a transcendência através de elegância pura",
            descricao_sensorial="Sublime Blanc é transcendência em branco. Bergamota e pera abrem luminosas, jasmim e flor de laranjeira desabrocham em sofisticação floral suprema, almíscar e cedro branco criam uma base celestial. Um aroma que eleva alma e marca presença com elegância divina.",
            cta_fechamento="Celebre com elegância suprema. Adquira Sublime Blanc!"
        ),
        mockup=MockupVisual(
            cor_cera="Branco Puro",
            hex_cera="#F5F5F5"
        )
    ),
]


def get_all_aromas() -> list[Aroma]:
    """Retorna a lista completa de todos os aromas do catálogo."""
    return CATALOGO_AROMAS


def get_aroma_by_id(id: str) -> Aroma | None:
    """Busca um aroma específico pelo ID. Retorna None se não encontrado."""
    for aroma in CATALOGO_AROMAS:
        if aroma.id == id:
            return aroma
    return None
