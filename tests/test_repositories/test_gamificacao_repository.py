import pytest
from repositories.gamificacao_repository import GamificacaoRepository

def test_gamificacao_repository(mock_db):
    repo = GamificacaoRepository(mock_db)
    
    mock_db.client.data_store["acoes_gamificacao"] = [
        {"id": 1, "nome": "completar_desafio", "pontos": 100}
    ]
    mock_db.client.data_store["niveis"] = [
        {"id": 1, "nome": "Iniciante", "pontos_minimos": 0},
        {"id": 2, "nome": "Veterano", "pontos_minimos": 100}
    ]
    
    # get_nivel_por_pontos
    novo_nivel = repo.get_nivel_por_pontos(150)
    assert novo_nivel["id"] == 2
    
    # registrar_pontuacao
    repo.registrar_pontuacao("aluno-1", "completar_desafio", "Desc")
    assert len(mock_db.client.data_store["pontuacoes"]) == 1
    
    # get_historico_pontos
    historico = repo.get_historico_pontos("aluno-1")
    assert len(historico) == 1
    
    # get_ranking_geral
    mock_db.client.data_store["ranking_geral_view"] = [
        {"aluno_id": "aluno-1", "pontos_total": 500}
    ]
    ranking = repo.get_ranking_geral()
    assert len(ranking) > 0
    assert ranking[0]["pontos_total"] == 500
