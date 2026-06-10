from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Union
from dependencies.auth import get_current_professor, get_current_aluno, get_current_user, get_database_provider
from models.user import ProfessorResponse, AlunoResponse
from models.mini_prova import (
    MiniProvaCreate, 
    MiniProvaResponse, 
    MiniProvaDetalhesResponse, 
    MiniProvaDetalhesPublicResponse,
    TentativaResponse,
    RespostaSubmit,
    ResultadoTentativaResponse
)
from services.mini_prova_service import MiniProvaService
from services.gamificacao_service import GamificacaoService
from services.missao_service import MissaoService
from providers.database_provider import DatabaseProvider

router = APIRouter(tags=["Mini-Provas"])

def get_gamificacao_service(db: DatabaseProvider = Depends(get_database_provider)) -> GamificacaoService:
    return GamificacaoService(db)

def get_missao_service(
    db: DatabaseProvider = Depends(get_database_provider),
    gamificacao_service: GamificacaoService = Depends(get_gamificacao_service)
) -> MissaoService:
    return MissaoService(db, gamificacao_service)

def get_mini_prova_service(
    db: DatabaseProvider = Depends(get_database_provider),
    gamificacao_service: GamificacaoService = Depends(get_gamificacao_service),
    missao_service: MissaoService = Depends(get_missao_service)
) -> MiniProvaService:
    return MiniProvaService(db, gamificacao_service, missao_service)

# ==========================================
# ROTAS DE PROVAS
# ==========================================

@router.post("/mini-provas", response_model=MiniProvaDetalhesResponse, status_code=status.HTTP_201_CREATED)
def criar_prova(
    data: MiniProvaCreate,
    professor: ProfessorResponse = Depends(get_current_professor),
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    return service.criar_prova(professor.id, data)

@router.get("/mini-provas/turma/{turma_id}", response_model=List[MiniProvaResponse])
def listar_provas_turma(
    turma_id: str,
    user = Depends(get_current_user), # Aluno ou Professor
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    return service.listar_provas_turma(turma_id)

@router.get("/mini-provas/{prova_id}")
def obter_prova_detalhes(
    prova_id: str,
    user = Depends(get_current_user),
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    """
    Retorna os detalhes da prova. 
    Se for professor, retorna com gabarito (MiniProvaDetalhesResponse).
    Se for aluno, retorna sem gabarito (MiniProvaDetalhesPublicResponse).
    """
    prova_completa = service.obter_prova_completa(prova_id)
    
    if isinstance(user, ProfessorResponse):
        return prova_completa
    else:
        # Pydantic vai ignorar os campos 'correta' ao instanciar o PublicResponse
        # Mas para garantir, usamos model_dump e validamos com a classe pública
        return MiniProvaDetalhesPublicResponse.model_validate(prova_completa.model_dump())

@router.post("/mini-provas/{prova_id}/iniciar", response_model=TentativaResponse, status_code=status.HTTP_201_CREATED)
def iniciar_tentativa(
    prova_id: str,
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    return service.iniciar_tentativa(aluno.id, prova_id)

# ==========================================
# ROTAS DE TENTATIVAS
# ==========================================

@router.post("/tentativas/{tentativa_id}/responder", response_model=TentativaResponse)
def submeter_respostas(
    tentativa_id: str,
    respostas: List[RespostaSubmit],
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    return service.submeter_respostas(aluno.id, tentativa_id, respostas)

@router.get("/tentativas/{tentativa_id}", response_model=ResultadoTentativaResponse)
def ver_resultado(
    tentativa_id: str,
    user = Depends(get_current_user),
    service: MiniProvaService = Depends(get_mini_prova_service)
):
    is_professor = isinstance(user, ProfessorResponse)
    return service.ver_resultado(tentativa_id, user.id, is_professor)
