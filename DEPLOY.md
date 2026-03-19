# Chamaroma Studio — Deploy Render + Vercel

Repositorio: [chamaroma-anapaula](https://github.com/aquinodigital-boop/chamaroma-anapaula)

## URLs alinhadas (padrao)

| Onde | Valor esperado |
|------|----------------|
| API Render | `https://chamaroma-anapaula-api.onrender.com` |
| Site Vercel | `https://chamaroma-anapaula.vercel.app` (ou a URL que o Vercel mostrar) |

Se o Render ou o Vercel gerarem outro endereco, atualize `frontend/vercel.json` e `ALLOWED_ORIGINS` no Render.

---

## Ordem recomendada

1. **Backend no Render** (primeiro)
2. **Frontend no Vercel** (depois)
3. **CORS no Render** com a URL final do Vercel

---

## 1. Backend no Render

### Blueprint ou manual
- [render.com](https://render.com) → **New** → **Blueprint** (se usar `render.yaml`) ou **Web Service**

### Configuracao
- **Name**: `chamaroma-anapaula-api` (assim a URL fica `https://chamaroma-anapaula-api.onrender.com`)
- **Root Directory**: `backend`
- **Runtime**: Python **3.11.7** (use `backend/runtime.txt` ou env `PYTHON_VERSION=3.11.7`)
- **Build Command** (copie exatamente):
  ```bash
  pip install --upgrade "pip>=24.0" setuptools wheel && pip install -r requirements.txt
  ```
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Se o build falhar com `pydantic-core` / `metadata-generation-failed`, quase sempre e pip antigo ou Python errado — confira os itens acima.

### Variaveis de ambiente
| Key | Valor |
|-----|-------|
| `GEMINI_API_KEY` | Sua chave Gemini |
| `PYTHON_VERSION` | `3.11.7` |
| `ALLOWED_ORIGINS` | Apos o passo do Vercel: `https://SUA-URL-VERCEL,http://localhost:5173` |

No primeiro deploy pode usar so `http://localhost:5173` e depois editar no Render quando o Vercel estiver no ar.

### Teste
Abra: `https://chamaroma-anapaula-api.onrender.com/api/health`  
(Se o nome do servico for outro, troque o subdominio.)

---

## 2. Frontend no Vercel

1. [vercel.com](https://vercel.com) → **Add New** → **Project** → importe o repo
2. **Root Directory**: `frontend`
3. **Framework**: Vite
4. **Build**: `npm run build`
5. **Output**: `dist`

### Proxy da API
O arquivo `frontend/vercel.json` ja aponta para:

`https://chamaroma-anapaula-api.onrender.com/api/:path*`

Se sua URL do Render for diferente, edite esse `destination`, faca commit e push.

---

## 3. CORS no Render (obrigatorio para o front funcionar)

No painel do servico → **Environment** → `ALLOWED_ORIGINS`:

```
https://chamaroma-anapaula.vercel.app,http://localhost:5173
```

Use exatamente a URL que o Vercel mostra em **Domains** (pode incluir `www` ou preview; para producao use o dominio principal).

Salve e aguarde o redeploy.

---

## 4. Escopo da versao

- CHAMAROMA only
- Categorias: `velas` e `home_spray`

---

## Checklist pos-deploy

- [ ] `GET .../api/health` OK no Render
- [ ] `GET .../api/aromas` retorna os aromas
- [ ] Site Vercel abre
- [ ] Catálogo carrega (sem erro de CORS)
- [ ] Geracao de prompts / imagens com `GEMINI_API_KEY` valida
