"""
Testes do endpoint /play_audio
Verifica se arquivos de áudio gerados podem ser baixados
"""

from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

client = TestClient(app)

TMP_DIR = Path("tmp")
TMP_DIR.mkdir(exist_ok=True)

def test_play_audio_file_exists():
    """
    Testa download de arquivo existente
    """
    test_file = TMP_DIR / "test_audio.mp3"
    test_file.write_bytes(b"dummy audio data")
    
    response = client.get("/play_audio/test_audio.mp3")
    
    assert response.status_code == 200
    assert response.content == b"dummy audio data"
    
    test_file.unlink()  # Remove arquivo após teste

def test_play_audio_file_not_found():
    """
    Testa erro ao tentar baixar arquivo inexistente
    """
    response = client.get("/play_audio/nonexistent.mp3")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
