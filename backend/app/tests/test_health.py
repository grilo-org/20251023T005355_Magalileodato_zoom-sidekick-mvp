"""
Testes do endpoint de saúde (/health)
Verifica se a API está respondendo corretamente
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Testa se o endpoint /health retorna status 200 e a mensagem correta
    """
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert "API is running" in json_data["message"]
