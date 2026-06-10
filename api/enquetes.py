from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependencies.auth import get_current_user, get_current_professor, get_current_aluno, get_database_provider
from models.enquete import EnqueteCreate, EnqueteResponse, VotoRequest
from models.user import ProfessorResponse, AlunoResponse
from services.enquete_service import EnqueteService
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/enquetes", tags=["Enquetes"])

def get_enquete_service(db: DatabaseProvider = Depends(get_database_provider)) -> EnqueteService:
    return EnqueteService(db)

@router.post("/", response_model=EnqueteResponse, status_code=status.HTTP_201_CREATED)
def criar_enquete(
    data: EnqueteCreate,
    prof: ProfessorResponse = Depends(get_current_professor),
    service: EnqueteService = Depends(get_enquete_service)
):
    return service.criar_enquete(prof.id, data)

@router.get("/turma/{turma_id}", response_model=List[EnqueteResponse])
def listar_enquetes_turma(
    turma_id: str,
    user = Depends(get_current_user),
    service: EnqueteService = Depends(get_enquete_service)
):
    # Pode ser visto tanto pelo professor quanto pelo aluno
    return service.listar_enquetes_turma(turma_id)

@router.get("/{enquete_id}", response_model=EnqueteResponse)
def obter_resultado_enquete(
    enquete_id: int,
    user = Depends(get_current_user),
    service: EnqueteService = Depends(get_enquete_service)
):
    return service.get_resultado(enquete_id)

@router.post("/{enquete_id}/votar", response_model=EnqueteResponse, status_code=status.HTTP_201_CREATED)
def votar_enquete(
    enquete_id: int,
    voto: VotoRequest,
    aluno: AlunoResponse = Depends(get_current_aluno),
    service: EnqueteService = Depends(get_enquete_service),
    db: DatabaseProvider = Depends(get_database_provider)
):
    # Garantir que o aluno pertence à turma da enquete
    enq = service.get_resultado(enquete_id)
    turma_aluno = db.client.table("turma_aluno").select("*").eq("turma_id", enq.turma_id).eq("aluno_id", aluno.id).execute()
    if not turma_aluno.data:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Aluno não pertence à turma desta enquete.")
        
    return service.votar(enquete_id, aluno.id, voto)
