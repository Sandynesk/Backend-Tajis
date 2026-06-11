from core.security import create_access_token

def test_criar_desafio_com_professor(client, mock_db):
    token = create_access_token(subject="prof-123", role="professor")
    
    response = client.post(
        "/desafios/",
        json={
            "titulo": "Novo Desafio API",
            "descricao": "Desc",
            "pontos": 100,
            "turma_id": "turma-1",
            "prazo": "2030-12-31T23:59:59Z",
            "disciplina_id": "disc-1"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Novo Desafio API"

def test_criar_desafio_com_aluno_rejeitado(client, mock_db):
    token = create_access_token(subject="aluno-123", role="aluno")
    
    response = client.post(
        "/desafios/",
        json={
            "titulo": "Desafio Inválido",
            "descricao": "Desc",
            "pontos": 100,
            "turma_id": "turma-1"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert "Requer privilégios de professor" in response.json()["detail"]
