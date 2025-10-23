"""
main.py - Ponto de entrada da aplicação FastAPI
------------------------------------------------
- Inicializa a API e middlewares
- Registra rotas
- Configura handlers globais de erro
- Serve frontend estático
"""

import traceback
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import shutil

from app.utils.logger import logger
from app.utils import config
from app.services import stt_service, tts_service, summary_service

# ------------------------
# Criação da aplicação
# ------------------------
app = FastAPI(
    title="Zoom Sidekick MVP",
    description="Assistente de entrevistas em reuniões online",
    version="1.0.0",
)

# ------------------------
# Middleware CORS
# ------------------------
allowed_origins = (
    ["*"] if config.ENVIRONMENT == "development" else (config.ALLOWED_ORIGINS or [])
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Middleware: handler global de exceções
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"[Unhandled Exception] Path: {request.url.path} | Error: {exc}\n"
        f"{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno. Contate o administrador."},
    )

# ------------------------
# Endpoints de Health
# ------------------------
@app.get("/api", tags=["Health"])
async def read_root():
    logger.info("Health check raiz solicitado")
    return {"status": "Zoom Sidekick API is running 🚀"}

@app.get("/api/health", tags=["Health"])
async def health_check():
    logger.info("Health check detalhado solicitado")
    return {
        "status": "ok",
        "env": config.ENVIRONMENT,
        "debug": config.DEBUG,
    }

# ------------------------
# Endpoint /answer - Recebe áudio e processa
# ------------------------
@app.post("/answer")
async def answer(audio: UploadFile = File(...)):
    """
    Recebe o áudio enviado pelo frontend, processa:
    1. Converte para WAV
    2. Transcreve (STT)
    3. Resume (GPT)
    4. Retorna JSON com transcrição, resumo e arquivo de áudio da próxima pergunta
    """
    try:
        # ------------------------
        # Pastas temporárias
        # ------------------------
        tmp_dir = Path("tmp")
        audio_dir = tmp_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        # ------------------------
        # Salvar arquivo enviado
        # ------------------------
        original_ext = Path(audio.filename).suffix
        input_path = audio_dir / f"input_{uuid4().hex}{original_ext}"
        with open(input_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        # ------------------------
        # Converter para WAV
        # ------------------------
        from app.utils.config_ffmpeg import AudioSegment
        wav_filename = f"response_{uuid4().hex}.wav"
        wav_path = audio_dir / wav_filename

        sound = AudioSegment.from_file(input_path)
        sound.export(wav_path, format="wav")

        # ------------------------
        # Processamento STT e Summary
        # ------------------------
        transcription = stt_service.transcribe(str(wav_path))
        summary = summary_service.summarize(transcription)

        # ------------------------
        # Próxima pergunta TTS
        # ------------------------
        next_question_text = "Qual sua experiência anterior?"
        next_audio_filename = f"question_{uuid4().hex}.wav"
        next_audio_path = audio_dir / next_audio_filename
        tts_service.generate_audio(next_question_text, str(next_audio_path))

        # ------------------------
        # Retornar JSON
        # ------------------------
        return {
            "transcription": transcription,
            "summary": summary,
            "next_question_audio": next_audio_filename
        }

    except Exception as e:
        logger.error(f"Erro ao processar /answer: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Erro ao processar áudio."}
        )

# ------------------------
# Endpoint para servir áudio da próxima pergunta
# ------------------------
@app.get("/play_audio/{filename}")
async def play_audio(filename: str):
    file_path = Path("tmp") / "audio" / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="audio/wav")
    return JSONResponse(status_code=404, content={"detail": "Arquivo de áudio não encontrado"})

# ------------------------
# Servir frontend estático
# ------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
    logger.info(f"Frontend montado em: {FRONTEND_DIR}")
