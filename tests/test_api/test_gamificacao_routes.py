from core.security import create_access_token

def test_get_ranking_geral(client, mock_db):
    token = create_access_token(subject="aluno-123", role="aluno")
    
    mock_db.client.data_store["ranking_geral_view"] = [
        {"aluno_id": "aluno-123", "nome_aluno": "João Aluno", "pontos_total": 500, "nivel_id": 2, "medalhas": 0}
    ]
    
    response = client.get(
        "/gamificacao/ranking",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert data[0]["pontos_total"] == 500

def test_ranking_sem_token(client):
    response = client.get("/gamificacao/ranking")
    assert response.status_code == 200
