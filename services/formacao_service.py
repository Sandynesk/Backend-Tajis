from typing import List, Optional
from fastapi import HTTPException, status
from providers.database_provider import DatabaseProvider
from repositories.formacao_repository import FormacaoRepository
from models.formacao import SessaoFormacaoCreate, SessaoFormacaoResponse
from core.algoritmos import balancear_grupos_zigzag
import logging

logger = logging.getLogger(__name__)

class FormacaoService:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.repo = FormacaoRepository(db)

    def gerar_formacao(self, professor_id: str, data: SessaoFormacaoCreate) -> SessaoFormacaoResponse:
        # 1. Obter alunos da turma
        res_turma = self.db.client.table("turma_aluno").select("aluno_id").eq("turma_id", data.turma_id).execute()
        aluno_ids = [a["aluno_id"] for a in res_turma.data]
        
        if not aluno_ids:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Turma não possui alunos.")
            
        # 2. Obter as métricas (pontuacao_total) da view
        res_alunos = self.db.client.table("ranking_geral_view")\
            .select("aluno_id, nome_aluno, pontos_total")\
            .in_("aluno_id", aluno_ids)\
            .order("pontos_total", desc=True)\
            .execute()
            
        alunos_rankeados = [
            {"id": a["aluno_id"], "nome": a["nome_aluno"], "pontuacao_total": a["pontos_total"]}
            for a in res_alunos.data
        ]
        
        # Inserir alunos que não pontuaram ainda (não estão na view) no final
        rankeados_ids = {a["id"] for a in alunos_rankeados}
        faltantes = list(set(aluno_ids) - rankeados_ids)
        if faltantes:
            res_base = self.db.client.table("aluno").select("id, nome").in_("id", faltantes).execute()
            for ab in res_base.data:
                alunos_rankeados.append({"id": ab["id"], "nome": ab["nome"], "pontuacao_total": 0})
                
        # 3. Executar o Algoritmo Balanceador (Zig-Zag)
        grupos_distribuidos = balancear_grupos_zigzag(alunos_rankeados, data.tamanho_grupo)
        
        if not grupos_distribuidos:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Falha ao gerar grupos balanceados.")

        # 4. Preparar payload para a RPC atômica
        sessao_data = {
            "turma_id": data.turma_id,
            "nome": data.nome,
            "professor_id": professor_id
        }
        
        sessao_id = self.repo.criar_sessao_atomo(sessao_data, grupos_distribuidos)
        if not sessao_id:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Falha na persistência atômica da formação.")
            
        # 5. Retornar a sessão completa recém-criada
        sessao_completa = self.repo.get_sessao_completa(sessao_id)
        return SessaoFormacaoResponse.model_validate(sessao_completa)

    def listar_sessoes_turma(self, turma_id: str) -> List[SessaoFormacaoResponse]:
        # Podemos retornar a sessão superficialmente ou completa. Para listar, só os dados base
        sessoes = self.repo.listar_sessoes_turma(turma_id)
        # O pydantic model pede grupos, passamos vazio na listagem simples.
        # Caso o front queira completos, precisariamos iterar get_sessao_completa (pode ser lento).
        return [SessaoFormacaoResponse.model_validate(s) for s in sessoes]

    def obter_sessao(self, sessao_id: int) -> SessaoFormacaoResponse:
        sessao = self.repo.get_sessao_completa(sessao_id)
        if not sessao:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sessão não encontrada")
        return SessaoFormacaoResponse.model_validate(sessao)

    def deletar_sessao(self, sessao_id: int):
        self.repo.deletar_sessao(sessao_id)
