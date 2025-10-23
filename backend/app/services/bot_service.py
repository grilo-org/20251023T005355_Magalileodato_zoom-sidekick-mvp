"""
Bot Service - Orquestração da Entrevista
----------------------------------------
Responsável por conduzir o fluxo da entrevista de forma automatizada:
1. Faz a pergunta ao usuário.
2. Recebe o áudio de resposta.
3. Converte para WAV (compatibilidade STT).
4. Transcreve o áudio (STT).
5. Resume a resposta (GPT).
6. Gera a próxima pergunta em áudio (TTS).
7. Retorna o áudio e o resumo.
"""

import logging
from pathlib import Path
from datetime import datetime
from uuid import uuid4
import warnings

# Ignora warnings específicos do PyDub sobre ffmpeg
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*")

from app.services import stt_service, tts_service, summary_service
from app.utils.config_ffmpeg import AudioSegment

logger = logging.getLogger(__name__)

TMP_DIR = Path("tmp")
TMP_DIR.mkdir(parents=True, exist_ok=True)

class InterviewBot:
    """
    Classe que representa o bot de entrevista.
    Mantém estado simples da conversa e orquestra serviços.
    """
    def __init__(self, questions=None):
        if questions is None:
            self.questions = [
                "Olá! Pode se apresentar brevemente?",
                "Quais são seus pontos fortes?",
                "Quais são seus pontos de melhoria?",
                "Fale sobre um projeto recente que você desenvolveu.",
                "Por que você quer trabalhar conosco?"
            ]
        else:
            self.questions = questions

        self.current_question_index = 0
        logger.info("InterviewBot inicializado com perguntas padrão")

    def get_next_question(self) -> str:
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            logger.info(f"Próxima pergunta: {question}")
            return question
        else:
            logger.info("Todas as perguntas foram feitas")
            return "Obrigado pela participação!"

    def process_response(self, audio_file: str) -> dict:
        logger.info("Processando resposta do usuário")

        wav_filename = f"response_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}.wav"
        wav_path = TMP_DIR / wav_filename

        try:
            audio = AudioSegment.from_file(audio_file)
            audio.export(wav_path, format="wav", codec="pcm_s16le")
            logger.info(f"Áudio convertido para WAV em: {wav_path}")
        except Exception as e:
            logger.error(f"Erro ao converter áudio: {e}")
            raise

        transcription = stt_service.transcribe(str(wav_path))
        logger.info(f"Transcrição obtida: {transcription[:50]}...")

        summary = summary_service.summarize(transcription)
        logger.info(f"Resumo gerado: {summary[:50]}...")

        next_question = self.get_next_question()
        try:
            audio_path = tts_service.generate_audio(next_question)
        except Exception as e:
            logger.error(f"Erro ao gerar áudio TTS: {e}")
            audio_path = ""

        return {
            "transcription": transcription,
            "summary": summary,
            "next_question_audio": audio_path
        }
