import pytest
from repositories.missao_repository import MissaoRepository, ProgressoMissaoRepository
from models.missao import MissaoCreate, EtapaMissaoCreate

def test_missao_repository(mock_db):
    repo = MissaoRepository(mock_db)
    
    # create
    etapa1 = EtapaMissaoCreate(ordem=1, descricao="Etapa 1", tipo_acao="acao1", meta=2, pontos_etapa=10)
    data = MissaoCreate(
        titulo="Missão 1",
        descricao="Desc",
        pontos_recompensa=100,
        tipo="individual",
        etapas=[etapa1]
    )
    criada = repo.create(data, "prof-1")
    assert criada["titulo"] == "Missão 1"
    
    # list_disponiveis
    mock_db.client.data_store["missoes"] = [
        {"id": 1, "titulo": "Missão 1", "ativa": True, "turma_id": None},
        {"id": 2, "titulo": "Missão 2", "ativa": False, "turma_id": None}
    ]
    ativas = repo.list_disponiveis()
    assert len(ativas) == 1
    assert ativas[0]["id"] == 1

def test_progresso_missao_repository(mock_db):
    repo = ProgressoMissaoRepository(mock_db)
    
    mock_db.client.data_store["progresso_missao"] = [
        {"id": 1, "aluno_id": "a1", "missao_id": 1, "etapa_atual": 1, "concluida": False}
    ]
    mock_db.client.data_store["progresso_etapa"] = [
        {"id": 1, "progresso_id": 1, "etapa_id": 1, "contador": 2, "concluida": False}
    ]
    
    # get_progresso
    prog = repo.get_progresso("a1", 1)
    assert prog["etapa_atual"] == 1
    assert len(prog["etapas_progresso"]) == 1
    
    # iniciar_missao
    iniciado = repo.iniciar_missao("a2", 2, [{"id": 2}])
    assert iniciado["etapa_atual"] == 1
    
    # get_missoes_em_andamento
    andamento = repo.get_missoes_em_andamento("a1")
    assert len(andamento) == 1
    
    # atualizar_contador_etapa
    repo.atualizar_contador_etapa(1, 3, True)
    
    # concluir_missao
    repo.concluir_missao(1)
    mock_db.client.data_store["progresso_missao"][0]["concluida"] = True
    concluida = repo.get_missoes_em_andamento("a1")
    assert len(concluida) == 0
