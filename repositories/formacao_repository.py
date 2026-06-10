from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
import logging

logger = logging.getLogger(__name__)

class FormacaoRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    def criar_sessao_atomo(self, sessao_data: Dict[str, Any], grupos_data: List[Dict[str, Any]]) -> Optional[int]:
        """
        Salva a sessão, os grupos e a distribuição de alunos numa única transação atômica 
        chamando a RPC `criar_sessao_formacao` do PostgreSQL.
        """
        try:
            res = self.db.client.rpc(
                "criar_sessao_formacao", 
                {"sessao_data": sessao_data, "grupos_data": grupos_data}
            ).execute()
            
            return res.data.get("sessao_id") if res.data else None
        except Exception as e:
            logger.error(f"Erro ao salvar formação atomicamente: {e}")
            raise e

    def listar_sessoes_turma(self, turma_id: str) -> List[Dict[str, Any]]:
        res = self.db.client.table("sessoes_formacao")\
            .select("*")\
            .eq("turma_id", turma_id)\
            .order("data_criacao", desc=True)\
            .execute()
        return res.data

    def get_sessao_completa(self, sessao_id: int) -> Optional[Dict[str, Any]]:
        # Busca sessão
        res_sessao = self.db.client.table("sessoes_formacao").select("*").eq("id", sessao_id).execute()
        if not res_sessao.data:
            return None
        sessao = res_sessao.data[0]
        
        # Busca grupos
        res_grupos = self.db.client.table("grupos").select("*").eq("sessao_id", sessao_id).execute()
        grupos = res_grupos.data
        
        # Busca alunos para os grupos (fazendo um join com a view de ranking ou tabela de aluno para ter o resumo)
        # Vamos usar a view de ranking_geral_view e juntar com a grupo_alunos manualmente ou em batch.
        grupo_ids = [g["id"] for g in grupos]
        if not grupo_ids:
            sessao["grupos"] = grupos
            return sessao
            
        res_galunos = self.db.client.table("grupo_alunos").select("*").in_("grupo_id", grupo_ids).execute()
        galunos = res_galunos.data
        
        # Para otimizar, busca o resumo dos alunos (pontuacao_total e nome) da view
        aluno_ids = list(set([ga["aluno_id"] for ga in galunos]))
        res_alunos = self.db.client.table("ranking_geral_view").select("aluno_id, nome_aluno, pontos_total").in_("aluno_id", aluno_ids).execute()
        alunos_dict = {a["aluno_id"]: {"id": a["aluno_id"], "nome": a["nome_aluno"], "pontuacao_total": a["pontos_total"]} for a in res_alunos.data}
        
        # Caso o aluno não tenha pontuação ainda (não está na view), busca da tabela base
        alunos_sem_ranking = [aid for aid in aluno_ids if aid not in alunos_dict]
        if alunos_sem_ranking:
            res_base = self.db.client.table("aluno").select("id, nome").in_("id", alunos_sem_ranking).execute()
            for ab in res_base.data:
                alunos_dict[ab["id"]] = {"id": ab["id"], "nome": ab["nome"], "pontuacao_total": 0}

        # Organiza nos grupos
        for g in grupos:
            g_alunos_ids = [ga["aluno_id"] for ga in galunos if ga["grupo_id"] == g["id"]]
            g["alunos"] = [alunos_dict[aid] for aid in g_alunos_ids if aid in alunos_dict]
            
        sessao["grupos"] = grupos
        return sessao

    def deletar_sessao(self, sessao_id: int):
        self.db.delete("sessoes_formacao", sessao_id)
