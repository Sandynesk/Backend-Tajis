def test_login_success(client):
    response = client.post(
        "/auth/login",
        json={"email": "joao@aluno.com", "senha": "senha123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client):
    response = client.post(
        "/auth/login",
        json={"email": "joao@aluno.com", "senha": "errada"}
    )
    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"]

def test_register_aluno(client):
    response = client.post(
        "/auth/register/aluno",
        json={"email": "novo.api@aluno.com", "senha": "senha123", "nome": "Novo", "matricula": "999"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "novo.api@aluno.com"
