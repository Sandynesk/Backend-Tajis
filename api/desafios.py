from fastapi import APIRouter, Depends, status
from typing import List
from dependencies.auth import get_current_professor, get_current_aluno, get_current_user, get_database_provider
from models.user import ProfessorResponse, AlunoResponse
from models.desafio import DesafioCreate, DesafioResponse, DesafioAlunoResponse, DesafioAlunoUpdate
from services.desafio_service import DesafioService
from services.gamificacao_service import GamificacaoService
from services.missao_service import MissaoService
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/desafios", tags=["Desafios"])

def get_gamificacao_service(db: DatabaseProvider = Depends(get_database_provider)) -> GamificacaoService:
    return GamificacaoService(db)

def get_missao_service(
    db: DatabaseProvider = Depends(get_database_provider),
    gamificacao_service: GamificacaoService = Depends(get_gamificacao_service)
) -> MissaoService:
    return MissaoService(db, gamificacao_service)

def get_desafio_service(
    db: DatabaseProvider = Depends(get_database_provider),
    gamificacao_service: GamificacaoService = Depends(get_gamificacao_service),
    missao_service: MissaoService = Depends(get_missao_service)
) -> DesafioService:
    return DesafioService(db, gamificacao_service, missao_service)

@router.post("/", response_model=DesafioResponse, status_code=status.HTTP_201_CREATED)
def criar_desafio(
    data: DesafioCreate,
    professor: ProfessorResponse = Depends(get_current_professor),
    service: DesafioService = Depends(get_desafio_service)
):
    return service.criar_desafio(professor.id, data)

@router.get("/turma/{turma_id}", response_model=List[DesafioResponse])
def listar_desafios_turma(
    turma_id: str,
    user = Depends(get_current_user), # Permite tanto aluno quanto professor
    service: DesafioService = Depends(get_desafio_service)
):
    return service.listar_desafios_turma(turma_id)

@router.post("/{desafio_id}/alunos/{aluno_id}", response_model=DesafioAlunoResponse)
def atribuir_aluno(
    desafio_id: str,
    aluno_id: str,
    professor: ProfessorResponse = Depends(get_current_professor),
    service: DesafioService = Depends(get_desafio_service)
):
    return service.atribuir_aluno(desafio_id, aluno_id)

@router.patch("/{desafio_id}/alunos/{aluno_id}", response_model=DesafioAlunoResponse)
def atualizar_status(
    desafio_id: str,
    aluno_id: str,
    data: DesafioAlunoUpdate,
    professor: ProfessorResponse = Depends(get_current_professor),
    service: DesafioService = Depends(get_desafio_service)
):
    # O professor pode atualizar o status/nota. Se a nota for enviada e o status omitido, assumimos concluído?
    # O service `concluir_desafio` já suporta isso. Mas `data.status` pode ser "pendente" ou "concluido".
    if data.status == "concluido" or data.nota is not None:
        return service.concluir_desafio(desafio_id, aluno_id, nota=data.nota)
    
    # Se for só alterar para pendente (reabrir), a lógica do repo já permite via update_status.
    # Mas se for só atualizar nota, passamos adiante.
    result = service.repo.update_status(desafio_id, aluno_id, data)
    return DesafioAlunoResponse.model_validate(result)

# Essa rota na verdade deveria estar em /alunos/me/desafios, mas podemos mapeá-la aqui para facilitar,
# ou então no app principal. Vamos mapeá-la aqui.
@router.get("/meus", response_model=List[DesafioAlunoResponse])
def listar_meus_desafios(
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: DesafioService = Depends(get_desafio_service)
):
    return service.listar_meus_desafios(aluno.id)
