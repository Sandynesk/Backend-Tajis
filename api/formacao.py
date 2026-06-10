from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependencies.auth import get_current_user, get_current_professor, get_current_aluno, get_database_provider
from models.formacao import SessaoFormacaoCreate, SessaoFormacaoResponse
from models.user import ProfessorResponse, AlunoResponse
from services.formacao_service import FormacaoService
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/formacao", tags=["Formacao"])

def get_formacao_service(db: DatabaseProvider = Depends(get_database_provider)) -> FormacaoService:
    return FormacaoService(db)

@router.post("/", response_model=SessaoFormacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_formacao(
    data: SessaoFormacaoCreate,
    prof: ProfessorResponse = Depends(get_current_professor),
    service: FormacaoService = Depends(get_formacao_service)
):
    """
    Cria uma nova sessão de formação. O último grupo pode ter menos integrantes se
    o número de alunos não for divisível pelo tamanho do grupo.
    """
    return service.gerar_formacao(prof.id, data)

@router.get("/turma/{turma_id}", response_model=List[SessaoFormacaoResponse])
def listar_sessoes_turma(
    turma_id: str,
    user = Depends(get_current_user),
    service: FormacaoService = Depends(get_formacao_service)
):
    return service.listar_sessoes_turma(turma_id)

@router.get("/{sessao_id}", response_model=SessaoFormacaoResponse)
def obter_sessao(
    sessao_id: int,
    user = Depends(get_current_user),
    service: FormacaoService = Depends(get_formacao_service)
):
    return service.obter_sessao(sessao_id)

@router.delete("/{sessao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_sessao(
    sessao_id: int,
    prof: ProfessorResponse = Depends(get_current_professor),
    service: FormacaoService = Depends(get_formacao_service)
):
    service.deletar_sessao(sessao_id)
