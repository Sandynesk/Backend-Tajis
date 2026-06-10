from fastapi import APIRouter, Depends, status
from models.user import AlunoCreate, AlunoResponse, ProfessorCreate, ProfessorResponse, LoginRequest, TokenResponse
from services.auth_service import AuthService
from dependencies.auth import get_database_provider
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_auth_service(db: DatabaseProvider = Depends(get_database_provider)) -> AuthService:
    return AuthService(db)

@router.post("/register/aluno", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def register_aluno(aluno: AlunoCreate, auth_service: AuthService = Depends(get_auth_service)):
    """Registra um novo aluno no sistema."""
    return auth_service.register_aluno(aluno)

@router.post("/register/professor", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
def register_professor(professor: ProfessorCreate, auth_service: AuthService = Depends(get_auth_service)):
    """Registra um novo professor no sistema."""
    return auth_service.register_professor(professor)

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """Autentica o usuário (aluno ou professor) e retorna o token JWT."""
    return auth_service.login(login_data)
