"""
config.py - Configuração centralizada do projeto
-----------------------------------------------
Responsável por:
- Carregar variáveis de ambiente (.env)
- Centralizar chaves sensíveis e configurações globais
- Facilitar manutenção e boas práticas (12-Factor App)
"""

# ------------------------
# Imports
# ------------------------
import os
from dotenv import load_dotenv

# ------------------------
# Carregar variáveis do .env
# ------------------------
# Carrega automaticamente variáveis de ambiente do arquivo .env
# Exemplo de .env:
# OPENAI_API_KEY=sk-xxxx
# DATABASE_URL=postgresql://user:pass@localhost/db
load_dotenv()

# ------------------------
# Configurações globais
# ------------------------
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # dev, staging, prod
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# ------------------------
# Validação básica
# ------------------------
if not OPENAI_API_KEY:
    raise ValueError("❌ Variável de ambiente OPENAI_API_KEY não encontrada no .env")

