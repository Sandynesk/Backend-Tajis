from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AlunoResumo(BaseModel):
    id: str
    nome: str
    pontuacao_total: int

class GrupoResponse(BaseModel):
    id: int
    nome: str
    alunos: List[AlunoResumo]

    model_config = {"from_attributes": True}

class SessaoFormacaoCreate(BaseModel):
    turma_id: str
    nome: str = Field(..., min_length=3, max_length=255)
    tamanho_grupo: int = Field(..., gt=0, description="Número de alunos por grupo")

class SessaoFormacaoResponse(BaseModel):
    id: int
    turma_id: str
    nome: str
    status: str
    data_criacao: datetime
    grupos: List[GrupoResponse] = []

    model_config = {"from_attributes": True}
