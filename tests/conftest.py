import pytest
from fastapi.testclient import TestClient
from main import app
from dependencies.auth import get_database_provider
from tests.mock_provider import MockProvider
from core.security import get_password_hash

@pytest.fixture(scope="function")
def mock_db():
    provider = MockProvider()
    
    # Setup inicial de dados comuns
    provider.client.data_store["aluno"] = [
        {
            "id": "aluno-123",
            "nome": "João Aluno",
            "email": "joao@aluno.com",
            "senha_hash": get_password_hash("senha123"),
            "matricula": "123456",
            "nivel_atual": 1,
            "xp_acumulado": 0,
            "criado_em": "2026-01-01T00:00:00Z"
        }
    ]
    
    provider.client.data_store["professor"] = [
        {
            "id": "prof-123",
            "nome": "Maria Professora",
            "email": "maria@prof.com",
            "senha_hash": get_password_hash("senha123"),
            "departamento": "TI",
            "criado_em": "2026-01-01T00:00:00Z"
        }
    ]

    provider.client.data_store["acoes_gamificacao"] = [
        {"id": 1, "nome": "completar_desafio", "pontos": 100},
        {"id": 2, "nome": "nota_maxima", "pontos": 300}
    ]
    
    return provider

@pytest.fixture(scope="function")
def client(mock_db):
    app.dependency_overrides[get_database_provider] = lambda: mock_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
