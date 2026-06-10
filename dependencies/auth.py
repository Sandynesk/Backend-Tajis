from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings
from providers import ProviderFactory
from repositories.aluno_repository import AlunoRepository
from repositories.professor_repository import ProfessorRepository
from models.user import AlunoResponse, ProfessorResponse
from typing import Union

# A URL do token é a rota de login que definiremos
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_database_provider():
    return ProviderFactory.create("supabase")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database_provider)) -> Union[AlunoResponse, ProfessorResponse]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if role == "aluno":
        aluno_repo = AlunoRepository(db)
        user = aluno_repo.get_by_id(user_id)
        if user is None:
            raise credentials_exception
        return AlunoResponse.model_validate(user)
        
    elif role == "professor":
        prof_repo = ProfessorRepository(db)
        user = prof_repo.get_by_id(user_id)
        if user is None:
            raise credentials_exception
        return ProfessorResponse.model_validate(user)
        
    else:
        raise credentials_exception

def get_current_aluno(current_user: Union[AlunoResponse, ProfessorResponse] = Depends(get_current_user)) -> AlunoResponse:
    if not isinstance(current_user, AlunoResponse):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de aluno"
        )
    return current_user

def get_current_professor(current_user: Union[AlunoResponse, ProfessorResponse] = Depends(get_current_user)) -> ProfessorResponse:
    if not isinstance(current_user, ProfessorResponse):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de professor"
        )
    return current_user
