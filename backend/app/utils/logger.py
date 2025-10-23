# backend/app/utils/logger.py
"""
Logger configurado com Loguru para o Zoom Sidekick MVP.

- Logs são enviados para console e arquivo rotativo.
- Níveis de logs podem ser ajustados conforme o ambiente (development/production).
- Mantém formato limpo e informações de data/hora.
"""

from loguru import logger
import sys
import os

# ------------------------
# Configuração de ambiente
# ------------------------
# Define o ambiente atual da aplicação. Pode ser "development" ou "production".
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# ------------------------
# Criação da pasta de logs
# ------------------------
# Garante que a pasta 'logs' exista antes de escrever arquivos
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ------------------------
# Remove logger padrão
# ------------------------
# Loguru já vem com um handler padrão (stdout). Vamos removê-lo para customizar
logger.remove()

# ------------------------
# Logger para console
# ------------------------
# Exibe logs no terminal
console_level = "DEBUG" if ENVIRONMENT == "development" else "INFO"
logger.add(
    sys.stdout,
    level=console_level,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
)

# ------------------------
# Logger para arquivo
# ------------------------
# Escreve logs em arquivo rotativo, mantendo histórico de 10 dias
file_level = "DEBUG" if ENVIRONMENT == "development" else "INFO"
logger.add(
    os.path.join(LOG_DIR, "zoom_sidekick.log"),
    rotation="5 MB",          # novo arquivo após 5MB
    retention="10 days",      # mantém 10 dias de logs
    level=file_level,
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
