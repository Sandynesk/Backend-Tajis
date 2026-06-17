from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependencies.auth import get_current_user, get_current_professor, get_current_aluno, get_database_provider
from models.missao import MissaoCreate, MissaoResponse, ProgressoMissaoResponse
from models.user import ProfessorResponse, AlunoResponse
from services.missao_service import MissaoService
from services.gamificacao_service import GamificacaoService
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/missoes", tags=["Missoes"])

# Fábrica de dependência como sugerido para evitar circularidade
def get_gamificacao_service(db: DatabaseProvider = Depends(get_database_provider)) -> GamificacaoService:
    return GamificacaoService(db)

def get_missao_service(
    db: DatabaseProvider = Depends(get_database_provider),
    gamificacao_service: GamificacaoService = Depends(get_gamificacao_service)
) -> MissaoService:
    return MissaoService(db, gamificacao_service)

@router.post("/", response_model=MissaoResponse, status_code=status.HTTP_201_CREATED)
def criar_missao(
    data: MissaoCreate,
    prof: ProfessorResponse = Depends(get_current_professor),
    service: MissaoService = Depends(get_missao_service)
):
    return service.criar_missao(prof.id, data)

@router.get("/disponiveis", response_model=List[MissaoResponse])
def listar_missoes_disponiveis(
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: MissaoService = Depends(get_missao_service),
    db: DatabaseProvider = Depends(get_database_provider)
):
    # Encontrar a qual turma o aluno pertence
    turmas_aluno = db.client.table("turma_aluno").select("turma_id").eq("aluno_id", aluno.id).execute()
    turma_id = turmas_aluno.data[0]["turma_id"] if turmas_aluno.data else None
    
    return service.listar_missoes_disponiveis(turma_id)

@router.get("/turma/{turma_id}", response_model=List[MissaoResponse])
def listar_missoes_turma(
    turma_id: str,
    user = Depends(get_current_user),
    service: MissaoService = Depends(get_missao_service)
):
    return service.listar_missoes_disponiveis(turma_id)

@router.post("/{missao_id}/iniciar", response_model=ProgressoMissaoResponse, status_code=status.HTTP_201_CREATED)
def iniciar_missao(
    missao_id: int,
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: MissaoService = Depends(get_missao_service)
):
    return service.iniciar_missao(aluno.id, missao_id)

@router.get("/{missao_id}/progresso", response_model=ProgressoMissaoResponse)
def ver_progresso(
    missao_id: int,
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: MissaoService = Depends(get_missao_service)
):
    return service.get_progresso(aluno.id, missao_id)
