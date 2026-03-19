# Imagem oficial = Python + pip corretos; evita build do pydantic-core a partir do fonte no Render
FROM python:3.11.7-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m pip install --upgrade "pip>=24.2" "setuptools>=69" "wheel>=0.43"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Render define a variavel PORT
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
