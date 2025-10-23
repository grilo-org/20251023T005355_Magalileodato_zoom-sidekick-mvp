from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.bot_service import InterviewBot
from app.utils.logger import logger
from pydub import AudioSegment  # <- para conversão webm → wav
import tempfile

# Inicializa o bot (perguntas padrão)
bot = InterviewBot()

# Criação do roteador do FastAPI
router = APIRouter()

# Diretório temporário para salvar arquivos de áudio
TMP_DIR = Path("tmp")
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Define tamanho máximo de arquivo de áudio (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


@router.get("/health", tags=["Health"], summary="Verifica se a API está rodando")
async def health_check():
    logger.info("Health check solicitado")
    return {"status": "ok", "message": "API is running"}


@router.get("/next_question", tags=["Interview"], summary="Retorna a próxima pergunta do bot")
def get_next_question():
    question = bot.get_next_question()
    logger.info(f"Próxima pergunta: {question}")
    return {
        "question": question,
        "question_index": bot.current_index,
        "finished": bot.is_finished()
    }


@router.post("/answer", tags=["Interview"], summary="Envia a resposta do usuário")
async def answer_question(audio: UploadFile = File(...)):
    logger.info(f"Recebido arquivo de áudio: {audio.filename} ({audio.content_type})")

    # Valida tipo de arquivo
    if audio.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3", "audio/webm"]:
        logger.warning(f"Tipo de arquivo inválido: {audio.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não suportado: {audio.content_type}"
        )

    # Valida tamanho do arquivo
    if audio.spool_max_size > MAX_FILE_SIZE:
        logger.warning(f"Arquivo muito grande: {audio.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo muito grande (máx. 5MB)"
        )

    try:
        # Se for WEBM → converter para WAV antes de processar
        if audio.content_type == "audio/webm":
            logger.info("Convertendo arquivo WEBM para WAV...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_webm:
                tmp_webm.write(await audio.read())
                tmp_webm.flush()
                wav_path = tmp_webm.name.replace(".webm", ".wav")

                AudioSegment.from_file(tmp_webm.name, format="webm").export(wav_path, format="wav")

            with open(wav_path, "rb") as f:
                result = bot.process_response(f)

        else:
            # Para arquivos já em WAV/MP3
            result = bot.process_response(audio.file)

        logger.info("Áudio processado com sucesso")

    except Exception as e:
        logger.error(f"Erro ao processar áudio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar áudio: {str(e)}"
        )

    return {
        "transcription": result.get("transcription"),
        "summary": result.get("summary"),
        "next_question_audio": result.get("next_question_audio")
    }


@router.get("/play_audio/{audio_filename}", tags=["Interview"], summary="Baixa ou reproduz um áudio gerado")
def play_audio(audio_filename: str):
    audio_path = TMP_DIR / audio_filename

    if not audio_path.exists():
        logger.warning(f"Arquivo não encontrado: {audio_filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )

    logger.info(f"Reproduzindo arquivo de áudio: {audio_filename}")
    return FileResponse(
        path=audio_path,
        filename=audio_filename,
        media_type="audio/mpeg"
    )
