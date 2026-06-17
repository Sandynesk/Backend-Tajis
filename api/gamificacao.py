from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependencies.auth import get_current_user, get_current_professor, get_current_aluno, get_database_provider
from models.gamificacao import RankingEntry, NivelResponse, MedalhaAlunoResponse, PontuacaoResponse, AcaoGamificacaoCreate, AcaoGamificacaoResponse
from models.user import ProfessorResponse
from services.gamificacao_service import GamificacaoService
from providers.database_provider import DatabaseProvider

router = APIRouter(prefix="/gamificacao", tags=["Gamificacao"])

def get_gamificacao_service(db: DatabaseProvider = Depends(get_database_provider)) -> GamificacaoService:
    return GamificacaoService(db)

@router.get("/pontuacoes/aluno/{aluno_id}", response_model=List[PontuacaoResponse])
def get_historico_pontos(
    aluno_id: str,
    user = Depends(get_current_user),
    service: GamificacaoService = Depends(get_gamificacao_service)
):
    if not isinstance(user, ProfessorResponse) and user.id != aluno_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")
    return service.listar_historico_pontos(aluno_id)

@router.get("/ranking", response_model=List[RankingEntry])
def get_ranking_geral(service: GamificacaoService = Depends(get_gamificacao_service)):
    # Ranking geral pode ser acessado por qualquer um (público)
    return service.obter_ranking_geral()

@router.get("/ranking/semanal", response_model=List[RankingEntry])
def get_ranking_semanal(service: GamificacaoService = Depends(get_gamificacao_service)):
    return service.obter_ranking_semanal()

@router.get("/alunos/{aluno_id}/medalhas", response_model=List[MedalhaAlunoResponse])
def get_medalhas_aluno(
    aluno_id: str,
    user = Depends(get_current_user),
    service: GamificacaoService = Depends(get_gamificacao_service)
):
    return service.listar_medalhas_aluno(aluno_id)

@router.get("/alunos/{aluno_id}/nivel", response_model=NivelResponse)
def get_nivel_aluno(
    aluno_id: str,
    user = Depends(get_current_user),
    service: GamificacaoService = Depends(get_gamificacao_service)
):
    nivel = service.verificar_nivel(aluno_id)
    if not nivel:
        raise HTTPException(status_code=404, detail="Nenhum nível alcançado ainda")
    return nivel

@router.get("/progresso/{aluno_id}")
def get_progresso_aluno(
    aluno_id: str,
    user = Depends(get_current_user),
    service: GamificacaoService = Depends(get_gamificacao_service),
    db: DatabaseProvider = Depends(get_database_provider)
):
    # Fetch total points from ranking view
    res = db.client.table("ranking_geral_view").select("pontos_total").eq("aluno_id", aluno_id).execute()
    pontos = res.data[0]["pontos_total"] if res.data else 0
    
    nivel = service.verificar_nivel(aluno_id)
    nivel_atual = nivel.id if nivel else 1
    
    # Counts (optional: we can query real tables or just default for MVP)
    desafios_res = db.client.table("solucoes_desafio").select("id", count="exact").eq("aluno_id", aluno_id).execute()
    missoes_res = db.client.table("progresso_missao").select("id", count="exact").eq("aluno_id", aluno_id).execute()
    
    return {
        "pontuacao": pontos,
        "nivel": nivel_atual,
        "desafios_completos": desafios_res.count if desafios_res.count else 0,
        "missoes_ativas": missoes_res.count if missoes_res.count else 0
    }

@router.post("/acoes", response_model=AcaoGamificacaoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_acao(
    acao: AcaoGamificacaoCreate,
    prof: ProfessorResponse = Depends(get_current_professor),
    service: GamificacaoService = Depends(get_gamificacao_service)
):
    # Insere ação usando repo genérico do provider, como a tabela é acoes_gamificacao
    result = service.db.insert("acoes_gamificacao", acao.model_dump())
    return AcaoGamificacaoResponse.model_validate(result)
