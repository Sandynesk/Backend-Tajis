import pytest
from repositories.aluno_repository import AlunoRepository
from core.security import get_password_hash

def test_aluno_repository_create_and_get(mock_db):
    repo = AlunoRepository(mock_db)
    
    # Criar
    aluno_data = {
        "nome": "Novo Aluno",
        "email": "novo@aluno.com",
        "senha_hash": get_password_hash("123"),
        "matricula": "999"
    }
    novo_aluno = repo.create(aluno_data)
    assert novo_aluno["email"] == "novo@aluno.com"
    assert "id" in novo_aluno
    
    # Buscar por id
    aluno_buscado = repo.get_by_id(novo_aluno["id"])
    assert aluno_buscado is not None
    assert aluno_buscado["nome"] == "Novo Aluno"
    
    # Buscar por email
    aluno_email = repo.get_by_email("novo@aluno.com")
    assert aluno_email is not None
    assert aluno_email["matricula"] == "999"
