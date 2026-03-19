# Chamaroma Studio — Deploy Render + Vercel

## 1. Backend no Render

### Criar o servico
1. Va em [render.com](https://render.com) -> **New Web Service**
2. Conecte o repositorio Git
3. Configure:
   - **Name**: `chamaroma-studio-api`
   - **Root Directory**: `backend`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Variaveis de ambiente
| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | Sua chave da API Gemini |
| `ALLOWED_ORIGINS` | `https://chamaroma-studio.vercel.app,http://localhost:5173` |
| `PYTHON_VERSION` | `3.11.7` |

Depois do deploy, anote a URL (exemplo: `https://chamaroma-studio-api.onrender.com`).

---

## 2. Frontend no Vercel

### Criar o projeto
1. Va em [vercel.com](https://vercel.com) -> **New Project**
2. Conecte o repositorio Git
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Rewrites de API
No arquivo `frontend/vercel.json`, mantenha:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://chamaroma-studio-api.onrender.com/api/:path*"
    }
  ]
}
```

---

## 3. Atualizar CORS no Render

Apos o frontend estar publicado, confirme no Render:
- `ALLOWED_ORIGINS` = `https://chamaroma-studio.vercel.app`

---

## 4. Escopo da versao final

- Produto focado somente em CHAMAROMA
- Categorias ativas: `velas` e `home_spray`
- Diretrizes de `tinta`, `ferramentas` e outros segmentos removidas

---

## 5. Checklist pos-deploy

- [ ] Backend responde em `https://xxx.onrender.com/api/health`
- [ ] Backend retorna 17 aromas em `https://xxx.onrender.com/api/aromas`
- [ ] Frontend carrega em `https://xxx.vercel.app`
- [ ] Aba Catalogo mostra os 17 aromas
- [ ] Geracao de prompts funciona (imagem + Gemini key valida)
- [ ] Geracao de imagens funciona
