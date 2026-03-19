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

## 1. Backend no Render (recomendado: Docker)

O ambiente **Native Python** do Render as vezes ignora o upgrade do `pip` (continua em 23.x) e ai o `pydantic-core` tenta compilar do fonte e falha. Por isso o repo usa **Docker** (`backend/Dockerfile`).

### Opcao A — Blueprint
1. [render.com](https://render.com) → **New** → **Blueprint**
2. Conecte o repo `chamaroma-anapaula`
3. Use o `render.yaml` na **raiz** do repositorio (Render detecta sozinho)
4. Preencha `GEMINI_API_KEY` (e depois `ALLOWED_ORIGINS`)

### Opcao B — Web Service manual com Docker
1. **New** → **Web Service** → mesmo repo
2. **Root Directory**: deixe **vazio** (raiz) **ou** `backend` conforme abaixo:
   - Se **Root Directory** = **vazio**: **Environment** = **Docker**, **Dockerfile Path** = `backend/Dockerfile`, **Docker Build Context** = `backend`
   - Se **Root Directory** = **`backend`**: **Dockerfile Path** = `Dockerfile`, **Docker Build Context** = `.`
3. **Name**: `chamaroma-anapaula-api`
4. Nao use mais Build/Start de Python nativo — o `CMD` do Dockerfile ja sobe o `uvicorn`

### Se voce ja tinha criado como Python nativo
Em **Settings** → mude **Environment** para **Docker** e configure Dockerfile + context como acima, depois **Manual Deploy**.

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
