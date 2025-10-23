# Etapa 1: Imagem base oficial do Python 3.11 slim
# Objetivo: Ter um ambiente leve com Python instalado
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instala dependências do Python
# Objetivo: Separar instalação de dependências para otimizar build
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia todo o backend para dentro do container
COPY . .

# Expõe a porta usada pelo FastAPI
EXPOSE 8000

# Define variável de ambiente para evitar buffering de logs
ENV PYTHONUNBUFFERED=1

# Comando padrão para iniciar a API
# Objetivo: Permitir que o container execute o backend automaticamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
