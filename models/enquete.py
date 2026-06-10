from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OpcaoEnqueteCreate(BaseModel):
    texto: str = Field(..., max_length=255)

class OpcaoEnqueteResponse(BaseModel):
    id: int
    texto: str
    contador: int
    percentual: float = 0.0

    model_config = {"from_attributes": True}

class EnqueteCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = None
    turma_id: str
    tipo: str = Field(..., pattern="^(unica|multipla)$")
    data_fim: Optional[datetime] = None
    opcoes: List[OpcaoEnqueteCreate] = Field(..., min_length=2)

class EnqueteResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    turma_id: str
    professor_id: str
    tipo: str
    ativa: bool
    data_criacao: datetime
    data_fim: Optional[datetime]
    opcoes: List[OpcaoEnqueteResponse] = []
    total_votantes: int = 0

    model_config = {"from_attributes": True}

class VotoRequest(BaseModel):
    opcoes_ids: List[int] = Field(..., min_length=1)
