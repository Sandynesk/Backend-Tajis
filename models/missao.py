from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EtapaMissaoCreate(BaseModel):
    ordem: int = Field(..., gt=0)
    descricao: str
    tipo_acao: str = Field(..., description="Nome da ação gamificada, ex: desafio_concluido")
    meta: int = Field(..., gt=0, description="Quantidade de vezes que a ação deve ser realizada")
    pontos_etapa: int = Field(0, ge=0)

class EtapaMissaoResponse(BaseModel):
    id: int
    ordem: int
    descricao: str
    tipo_acao: str
    meta: int
    pontos_etapa: int

    model_config = {"from_attributes": True}

class MissaoCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: str
    turma_id: Optional[str] = None
    tipo: str = Field(..., pattern="^(individual|turma)$")
    pontos_recompensa: int = Field(0, ge=0)
    etapas: List[EtapaMissaoCreate]

class MissaoResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    professor_id: str
    turma_id: Optional[str] = None
    ativa: bool
    tipo: str
    pontos_recompensa: int
    data_criacao: datetime
    data_fim: Optional[datetime] = None
    etapas: Optional[List[EtapaMissaoResponse]] = None

    model_config = {"from_attributes": True}

class ProgressoEtapaResponse(BaseModel):
    id: int
    progresso_id: int
    etapa_id: int
    contador: int
    concluida: bool
    etapa: Optional[EtapaMissaoResponse] = None

    model_config = {"from_attributes": True}

class ProgressoMissaoResponse(BaseModel):
    id: int
    aluno_id: str
    missao_id: int
    etapa_atual: int
    concluida: bool
    data_inicio: datetime
    data_conclusao: Optional[datetime] = None
    etapas_progresso: Optional[List[ProgressoEtapaResponse]] = None

    model_config = {"from_attributes": True}
