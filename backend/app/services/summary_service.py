"""
Summary Service - Resumo de Texto
---------------------------------
Responsável por resumir textos de forma automática utilizando a API da OpenAI (GPT).
Este módulo é isolado para facilitar manutenção, testes e evolução do código.
"""

import os
import logging
import openai
from dotenv import load_dotenv

# Configuração do logger para este módulo
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da OpenAI a partir do .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.warning("Chave OPENAI_API_KEY não encontrada no .env")
else:
    openai.api_key = OPENAI_API_KEY
    logger.info("OpenAI API Key carregada com sucesso")

def summarize(text: str, max_tokens: int = 100) -> str:
    """
    Recebe um texto e retorna um resumo conciso usando GPT.

    Parâmetros:
    ----------
    text : str
        Texto que será resumido.
    max_tokens : int, opcional
        Número máximo de tokens para o resumo (default=100).

    Retorna:
    -------
    str
        Texto resumido gerado pelo GPT.
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API Key não configurada. Retornando texto original.")
        return text

    try:
        # Chamada à API da OpenAI para gerar resumo
        response = openai.Completion.create(
            engine="text-davinci-003",        # Modelo GPT
            prompt=f"Resuma o seguinte texto:\n{text}",
            max_tokens=max_tokens,
            temperature=0.7,
        )
        summary = response.choices[0].text.strip()
        logger.info(f"Resumo gerado com sucesso: {summary[:50]}...")  # Log das primeiras palavras
        return summary
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        return text
