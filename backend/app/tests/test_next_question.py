"""
Testes do endpoint /next_question
Verifica o fluxo inicial e continuidade da entrevista
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_next_question():
    """
    Testa se o endpoint retorna a primeira pergunta
    """
    response = client.get("/next_question")
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "question_index" in data
    assert "finished" in data
    assert isinstance(data["question"], str)
    assert isinstance(data["question_index"], int)
    assert isinstance(data["finished"], bool)
