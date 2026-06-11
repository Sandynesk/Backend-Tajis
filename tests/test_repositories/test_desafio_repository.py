import pytest
from repositories.desafio_repository import DesafioRepository
from models.desafio import DesafioCreate, DesafioAlunoUpdate

def test_desafio_repository_create_and_get(mock_db):
    repo = DesafioRepository(mock_db)
    
    data = DesafioCreate(
        titulo="Desafio de Teste",
        descricao="Faça algo legal",
        pontos=500,
        turma_id="turma-x",
        prazo="2030-12-31T23:59:59Z",
        disciplina_id="disc-y"
    )
    
    # Create
    criado = repo.create(data, "prof-1")
    assert criado["titulo"] == "Desafio de Teste"
    assert "id" in criado
    
    # Get by id
    buscado = repo.get_by_id(criado["id"])
    assert buscado is not None
    assert buscado["pontos"] == 500
    
    # List by turma
    desafios = repo.list_by_turma("turma-x")
    assert len(desafios) == 1
    assert desafios[0]["titulo"] == "Desafio de Teste"
    
    # Assign to aluno
    mock_db.client.data_store["desafios_alunos"] = []
    repo.assign_to_aluno(criado["id"], "aluno-1")
    assert len(mock_db.client.data_store["desafios_alunos"]) == 1

def test_desafio_update_and_get(mock_db):
    repo = DesafioRepository(mock_db)
    mock_db.client.data_store["desafios_alunos"] = [
        {"id": "atrib-1", "aluno_id": "aluno-z", "desafio_id": "des-y", "status": "pendente"}
    ]
    
    # Get atribuicao
    atrib = repo.get_atribuicao("des-y", "aluno-z")
    assert atrib is not None
    assert atrib["status"] == "pendente"
    
    # Update status
    update_data = DesafioAlunoUpdate(status="concluido")
    atualizado = repo.update_status("des-y", "aluno-z", update_data)
    assert atualizado["status"] == "concluido"
    assert "data_conclusao" in atualizado
    
    # Get aluno desafios
    aluno_des = repo.get_aluno_desafios("aluno-z")
    assert len(aluno_des) == 1
