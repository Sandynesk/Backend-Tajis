import pytest
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from freezegun import freeze_time
from services.mini_prova_service import MiniProvaService
from services.gamificacao_service import GamificacaoService
from services.missao_service import MissaoService
from models.mini_prova import RespostaSubmit

def test_submeter_respostas_no_prazo(mock_db):
    gam_svc = GamificacaoService(mock_db)
    mis_svc = MissaoService(mock_db, gam_svc)
    service = MiniProvaService(mock_db, gam_svc, mis_svc)
    
    # Prepara dados
    prova_id = "prova-123"
    tentativa_id = "tent-123"
    aluno_id = "aluno-1"
    
    mock_db.client.data_store["mini_provas"] = [{
        "id": prova_id,
        "titulo": "Prova de Teste",
        "turma_id": "turma-1",
        "tempo_limite_segundos": 60, # 1 minuto
        "nota_minima_aprovacao": 0.7,
        "professor_id": "prof-1"
    }]
    
    mock_db.client.data_store["questoes"] = [
        {
            "id": "q1", "mini_prova_id": prova_id, "tipo": "multipla_escolha", "pontuacao": 10.0,
            "alternativas": [{"letra": "A", "correta": True}, {"letra": "B", "correta": False}]
        }
    ]
    
    mock_db.client.data_store["tentativas"] = [{
        "id": tentativa_id,
        "mini_prova_id": prova_id,
        "aluno_id": aluno_id,
        "data_inicio": datetime.now(timezone.utc).isoformat(),
        "concluida": False
    }]
    
    # Submete respostas corretas dentro do prazo
    respostas = [RespostaSubmit(questao_id="q1", alternativa_escolhida="A")]
    resultado = service.submeter_respostas(aluno_id, tentativa_id, respostas)
    
    assert resultado.concluida is True
    assert resultado.nota_final == 10.0

@freeze_time("2026-06-11 12:00:00", tz_offset=0)
def test_submeter_respostas_fora_do_prazo(mock_db):
    gam_svc = GamificacaoService(mock_db)
    mis_svc = MissaoService(mock_db, gam_svc)
    service = MiniProvaService(mock_db, gam_svc, mis_svc)
    
    prova_id = "prova-123"
    tentativa_id = "tent-out"
    aluno_id = "aluno-1"
    
    # Tempo limite = 60s. Data de início foi há 2 minutos (120s atrás)
    inicio_antigo = (datetime.now(timezone.utc) - timedelta(minutes=2)).isoformat()
    
    mock_db.client.data_store["mini_provas"] = [{
        "id": prova_id,
        "tempo_limite_segundos": 60,
        "questoes": []
    }]
    
    mock_db.client.data_store["tentativas"] = [{
        "id": tentativa_id,
        "mini_prova_id": prova_id,
        "aluno_id": aluno_id,
        "data_inicio": inicio_antigo,
        "concluida": False
    }]
    
    respostas = []
    
    with pytest.raises(HTTPException) as excinfo:
        service.submeter_respostas(aluno_id, tentativa_id, respostas)
        
    assert excinfo.value.status_code == 400
    assert "Tempo esgotado" in excinfo.value.detail
