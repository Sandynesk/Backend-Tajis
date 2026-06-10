from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class AlternativaCreate(BaseModel):
    letra: str = Field(..., max_length=1)
    texto: str
    correta: bool

class QuestaoCreate(BaseModel):
    enunciado: str
    tipo: str = Field(..., pattern="^(multipla_escolha|verdadeiro_falso|dissertativa)$")
    alternativas: Optional[List[AlternativaCreate]] = None
    pontuacao: float = Field(1.0, ge=0)

class MiniProvaCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = None
    turma_id: str
    tempo_limite_segundos: int = Field(300, gt=0) # Padrão de 5 minutos
    nota_minima_aprovacao: float = Field(0.7, ge=0.0, le=1.0)
    questoes: List[QuestaoCreate]

class MiniProvaResponse(BaseModel):
    id: str
    titulo: str
    descricao: Optional[str]
    professor_id: str
    turma_id: str
    tempo_limite_segundos: int
    nota_minima_aprovacao: float
    data_criacao: datetime

    model_config = {"from_attributes": True}

class AlternativaPublicResponse(BaseModel):
    letra: str
    texto: str
    
    model_config = {"from_attributes": True}

class AlternativaResponse(AlternativaPublicResponse):
    correta: bool

class QuestaoPublicResponse(BaseModel):
    id: str
    mini_prova_id: str
    enunciado: str
    tipo: str
    pontuacao: float
    alternativas: Optional[List[AlternativaPublicResponse]] = None

    model_config = {"from_attributes": True}

class QuestaoResponse(BaseModel):
    id: str
    mini_prova_id: str
    enunciado: str
    tipo: str
    pontuacao: float
    alternativas: Optional[List[AlternativaResponse]] = None

    model_config = {"from_attributes": True}

class MiniProvaDetalhesPublicResponse(MiniProvaResponse):
    questoes: List[QuestaoPublicResponse]

class MiniProvaDetalhesResponse(MiniProvaResponse):
    questoes: List[QuestaoResponse]

class TentativaResponse(BaseModel):
    id: str
    mini_prova_id: str
    aluno_id: str
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    nota_final: Optional[float] = None
    concluida: bool

    model_config = {"from_attributes": True}

class RespostaSubmit(BaseModel):
    questao_id: str
    alternativa_escolhida: Optional[str] = Field(None, max_length=1)
    texto_resposta: Optional[str] = None

class RespostaResponse(BaseModel):
    id: str
    tentativa_id: str
    questao_id: str
    alternativa_escolhida: Optional[str]
    texto_resposta: Optional[str]

    model_config = {"from_attributes": True}

class ResultadoTentativaResponse(BaseModel):
    tentativa: TentativaResponse
    respostas: List[RespostaResponse]
    prova: MiniProvaDetalhesResponse # Opcional: pode retornar as questões com gabarito para visualização após concluir
