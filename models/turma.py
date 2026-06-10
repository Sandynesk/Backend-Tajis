from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TurmaCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    disciplina_id: str
    professor_id: Optional[str] = None

class TurmaResponse(BaseModel):
    id: str
    nome: str
    disciplina_id: str
    professor_id: Optional[str]
    criado_em: datetime

    model_config = {"from_attributes": True}
