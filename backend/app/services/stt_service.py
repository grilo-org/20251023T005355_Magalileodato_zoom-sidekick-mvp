"""
STT Service - Speech to Text
-----------------------------
Usa Whisper para transcrever áudio em texto.
"""
import whisper
import logging

logger = logging.getLogger(__name__)

# Carrega modelo Whisper uma vez
try:
    model = whisper.load_model("base")
    logger.info("Modelo Whisper carregado com sucesso")
except Exception as e:
    logger.error(f"Falha ao carregar modelo Whisper: {e}")
    model = None

def transcribe(audio_file) -> str:
    """Converte áudio em texto."""
    if model is None:
        logger.warning("Modelo não carregado, retornando string vazia")
        return ""
    try:
        result = model.transcribe(audio_file)
        text = result.get("text", "").strip()
        logger.info(f"Transcrição concluída: {text[:50]}...")
        return text
    except Exception as e:
        logger.error(f"Erro ao transcrever áudio: {e}")
        return ""
