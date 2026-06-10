from pydantic import BaseModel, Field
from datetime import datetime

class DisciplinaCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    codigo: str = Field(..., max_length=50)

class DisciplinaResponse(BaseModel):
    id: str
    nome: str
    codigo: str
    criado_em: datetime

    model_config = {"from_attributes": True}
