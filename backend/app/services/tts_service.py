"""
TTS Service - Text to Speech
-----------------------------
Responsável por converter texto em áudio (fala) para o usuário.
Usa a biblioteca gTTS (Google Text-to-Speech) para gerar arquivos MP3.
Este módulo é isolado para facilitar manutenção e testes.
"""

from gtts import gTTS
import uuid
import os
import logging

# Configuração do logger para este módulo
logger = logging.getLogger(__name__)

# Diretório temporário para salvar arquivos de áudio gerados
TMP_AUDIO_DIR = "tmp"
if not os.path.exists(TMP_AUDIO_DIR):
    os.makedirs(TMP_AUDIO_DIR)
    logger.info(f"Pasta temporária criada em: {TMP_AUDIO_DIR}")

def generate_audio(text: str, lang: str = "pt") -> str:
    """
    Recebe um texto e gera um arquivo de áudio (MP3) com a fala correspondente.

    Parâmetros:
    ----------
    text : str
        Texto que será convertido em áudio.
    lang : str, opcional
        Código do idioma (default é 'pt' para português).

    Retorna:
    -------
    str
        Caminho do arquivo de áudio gerado.
    """
    try:
        # Gera um nome único para o arquivo de áudio
        filename = f"speech_{uuid.uuid4()}.mp3"
        filepath = os.path.join(TMP_AUDIO_DIR, filename)

        # Cria o objeto gTTS e salva o arquivo
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        logger.info(f"Áudio TTS gerado com sucesso: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Erro ao gerar áudio TTS: {e}")
        return ""
