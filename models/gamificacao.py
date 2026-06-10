from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AcaoGamificacaoCreate(BaseModel):
    nome: str = Field(..., max_length=255)
    pontos: int = Field(..., ge=0)

class AcaoGamificacaoResponse(BaseModel):
    id: int
    nome: str
    pontos: int

    model_config = {"from_attributes": True}

class PontuacaoResponse(BaseModel):
    id: int
    aluno_id: str
    acao_id: int
    pontos_ganhos: int
    data: datetime
    descricao: Optional[str] = None

    model_config = {"from_attributes": True}

class NivelResponse(BaseModel):
    id: int
    nome: str
    pontos_minimos: int
    icon: Optional[str] = None

    model_config = {"from_attributes": True}

class MedalhaCreate(BaseModel):
    nome: str = Field(..., max_length=255)
    descricao: str
    criterio: str
    icon: Optional[str] = None

class MedalhaResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    criterio: str
    icon: Optional[str] = None

    model_config = {"from_attributes": True}

class MedalhaAlunoResponse(BaseModel):
    id: int
    aluno_id: str
    medalha_id: int
    data_concedida: datetime
    medalha: Optional[MedalhaResponse] = None

    model_config = {"from_attributes": True}

class RankingEntry(BaseModel):
    posicao: int
    aluno_id: str
    nome_aluno: str
    pontos_total: int
    nivel_atual: Optional[str] = None
    medalhas: int = 0
