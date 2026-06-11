import pytest
from fastapi import HTTPException
from services.auth_service import AuthService
from models.user import AlunoCreate, LoginRequest

def test_login_success(mock_db):
    auth_service = AuthService(mock_db)
    
    login_aluno = LoginRequest(email="joao@aluno.com", senha="senha123")
    token_aluno = auth_service.login(login_aluno)
    assert token_aluno.role == "aluno"
    assert token_aluno.access_token is not None

    login_prof = LoginRequest(email="maria@prof.com", senha="senha123")
    token_prof = auth_service.login(login_prof)
    assert token_prof.role == "professor"
    assert token_prof.access_token is not None

def test_login_failure(mock_db):
    auth_service = AuthService(mock_db)
    
    # Senha errada
    with pytest.raises(HTTPException) as excinfo:
        auth_service.login(LoginRequest(email="joao@aluno.com", senha="errada"))
    assert excinfo.value.status_code == 401
    
    # Usuário inexistente
    with pytest.raises(HTTPException) as excinfo:
        auth_service.login(LoginRequest(email="naoexiste@email.com", senha="senha123"))
    assert excinfo.value.status_code == 401

def test_register_aluno(mock_db):
    auth_service = AuthService(mock_db)
    
    # Registro sucesso
    data = AlunoCreate(email="novo@aluno.com", senha="senha123", nome="Novo", matricula="111")
    aluno = auth_service.register_aluno(data)
    assert aluno.email == "novo@aluno.com"
    
    # Registro duplicado
    with pytest.raises(HTTPException) as excinfo:
        auth_service.register_aluno(AlunoCreate(email="joao@aluno.com", senha="senha123", nome="Joao", matricula="222"))
    assert excinfo.value.status_code == 400
    assert "já cadastrado" in excinfo.value.detail
