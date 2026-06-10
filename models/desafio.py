from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DesafioCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: str
    pontos: int = Field(..., gt=0, description="Pontos do desafio, deve ser maior que 0")
    turma_id: str = Field(..., description="UUID da turma")

class DesafioResponse(BaseModel):
    id: str
    titulo: str
    descricao: str
    pontos: int
    professor_id: str
    turma_id: str
    data_criacao: datetime

    model_config = {"from_attributes": True}

class DesafioAlunoUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(pendente|concluido)$")
    nota: Optional[float] = Field(None, ge=0)

class DesafioAlunoResponse(BaseModel):
    id: str
    desafio_id: str
    aluno_id: str
    status: str
    data_conclusao: Optional[datetime] = None
    nota: Optional[float] = None

    model_config = {"from_attributes": True}
