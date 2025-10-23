"""
Testes do endpoint /answer
Verifica envio de arquivo de áudio, transcrição e resumo
"""

from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO

client = TestClient(app)

def test_answer_with_valid_audio():
    """
    Testa envio de arquivo WAV válido e verifica resposta do bot
    """
    audio_content = BytesIO(b"fake audio data")  # Simula arquivo de áudio
    files = {"audio": ("test.wav", audio_content, "audio/wav")}
    response = client.post("/answer", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert "summary" in data
    assert "next_question_audio" in data

def test_answer_with_invalid_file_type():
    """
    Testa envio de arquivo inválido e espera erro
    """
    fake_file = BytesIO(b"not audio")
    files = {"audio": ("test.txt", fake_file, "text/plain")}
    response = client.post("/answer", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
