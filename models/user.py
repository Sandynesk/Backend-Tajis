from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- Schemas Genéricos de Autenticação ---
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# --- Schemas de Aluno ---
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")

class AlunoResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    nivel_atual: int
    xp_acumulado: int
    criado_em: datetime

    model_config = {"from_attributes": True}

# --- Schemas de Professor ---
class ProfessorCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")
    departamento: Optional[str] = None

class ProfessorResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    departamento: Optional[str]
    criado_em: datetime

    model_config = {"from_attributes": True}
