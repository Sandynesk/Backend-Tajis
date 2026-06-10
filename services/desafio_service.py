from typing import List
from fastapi import HTTPException, status
from providers.database_provider import DatabaseProvider
from repositories.desafio_repository import DesafioRepository
from repositories.professor_repository import ProfessorRepository
from models.desafio import DesafioCreate, DesafioResponse, DesafioAlunoResponse, DesafioAlunoUpdate
from services.gamificacao_service import GamificacaoService
from services.missao_service import MissaoService
from core.constants import ACAO_DESAFIO_CONCLUIDO

class DesafioService:
    def __init__(self, db: DatabaseProvider, gamificacao_service: GamificacaoService, missao_service: MissaoService):
        self.db = db
        self.repo = DesafioRepository(db)
        self.prof_repo = ProfessorRepository(db)
        self.gamificacao_service = gamificacao_service
        self.missao_service = missao_service

    def criar_desafio(self, professor_id: str, data: DesafioCreate) -> DesafioResponse:
        prof = self.prof_repo.get_by_id(professor_id)
        if not prof:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
            
        result = self.repo.create(data, professor_id)
        return DesafioResponse.model_validate(result)

    def listar_desafios_turma(self, turma_id: str) -> List[DesafioResponse]:
        results = self.repo.list_by_turma(turma_id)
        return [DesafioResponse.model_validate(r) for r in results]

    def atribuir_aluno(self, desafio_id: str, aluno_id: str) -> DesafioAlunoResponse:
        desafio = self.repo.get_by_id(desafio_id)
        if not desafio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desafio não encontrado")
            
        existente = self.repo.get_atribuicao(desafio_id, aluno_id)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno já atribuído a este desafio")
            
        result = self.repo.assign_to_aluno(desafio_id, aluno_id)
        return DesafioAlunoResponse.model_validate(result)

    def concluir_desafio(self, desafio_id: str, aluno_id: str, nota: float = None) -> DesafioAlunoResponse:
        atribuicao = self.repo.get_atribuicao(desafio_id, aluno_id)
        if not atribuicao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atribuição não encontrada")
            
        if atribuicao.get("status") == "concluido":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Desafio já concluído")
            
        update_data = DesafioAlunoUpdate(status="concluido", nota=nota)
        result = self.repo.update_status(desafio_id, aluno_id, update_data)
        
        # Gamificação e Missões
        if result:
            self.gamificacao_service.conceder_pontos(aluno_id, ACAO_DESAFIO_CONCLUIDO, f"Desafio concluído: {desafio_id}")
            self.missao_service.notificar_acao(aluno_id, ACAO_DESAFIO_CONCLUIDO)
            
        return DesafioAlunoResponse.model_validate(result)

    def listar_meus_desafios(self, aluno_id: str) -> List[DesafioAlunoResponse]:
        results = self.repo.get_aluno_desafios(aluno_id)
        return [DesafioAlunoResponse.model_validate(r) for r in results]
