"""
Serviço responsável por transcrever áudio em texto.
Pode usar Whisper (OpenAI) ou Vosk (open-source).
"""

import whisper

# Carrega o modelo uma única vez (boa prática)
model = whisper.load_model("base")

def transcribe(audio_file) -> str:
    """
    Recebe um arquivo de áudio e retorna o texto transcrito.
    """
    result = model.transcribe(audio_file)
    return result["text"]
