from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
import logging

logger = logging.getLogger(__name__)

class GamificacaoRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    # ==========================
    # AÇÕES E PONTUAÇÕES
    # ==========================
    def get_acao_por_nome(self, nome_acao: str) -> Optional[Dict[str, Any]]:
        results = self.db.fetch_all("acoes_gamificacao", filters={"nome": nome_acao}, limit=1)
        return results[0] if results else None

    def registrar_pontuacao(self, aluno_id: str, acao_nome: str, descricao: Optional[str] = None) -> Optional[Dict[str, Any]]:
        acao = self.get_acao_por_nome(acao_nome)
        if not acao:
            logger.warning(f"Ação de gamificação não encontrada: {acao_nome}")
            return None
            
        data = {
            "aluno_id": aluno_id,
            "acao_id": acao["id"],
            "pontos_ganhos": acao["pontos"],
            "descricao": descricao
        }
        return self.db.insert("pontuacoes", data)

    def get_historico_pontos(self, aluno_id: str) -> List[Dict[str, Any]]:
        # Fazer join manual no python ou buscar pontuacoes e ações separadamente
        response = self.db.client.table("pontuacoes")\
            .select("id, aluno_id, acao_id, pontos_ganhos, data, descricao")\
            .eq("aluno_id", aluno_id)\
            .order("data", desc=True)\
            .execute()
        return response.data

    # ==========================
    # NÍVEIS
    # ==========================
    def get_nivel_por_pontos(self, pontos_total: int) -> Optional[Dict[str, Any]]:
        response = self.db.client.table("niveis")\
            .select("*")\
            .lte("pontos_minimos", pontos_total)\
            .order("pontos_minimos", desc=True)\
            .limit(1)\
            .execute()
        return response.data[0] if response.data else None

    # ==========================
    # MEDALHAS
    # ==========================
    def conceder_medalha(self, aluno_id: str, medalha_id: int) -> Optional[Dict[str, Any]]:
        """ Tenta conceder a medalha ignorando se já existir graças ao UNIQUE do banco """
        data = {
            "aluno_id": aluno_id,
            "medalha_id": medalha_id
        }
        try:
            return self.db.insert("medalhas_alunos", data)
        except Exception as e:
            # Idempotência: se falhar por UNIQUE constraint, ignora.
            logger.debug(f"Medalha {medalha_id} já concedida ao aluno {aluno_id}. Erro ignorado: {e}")
            return None

    def get_medalhas_aluno(self, aluno_id: str) -> List[Dict[str, Any]]:
        response = self.db.client.table("medalhas_alunos")\
            .select("id, aluno_id, medalha_id, data_concedida")\
            .eq("aluno_id", aluno_id)\
            .execute()
            
        # Busca detalhes das medalhas
        if not response.data:
            return []
            
        medalhas_ids = [m["medalha_id"] for m in response.data]
        medalhas_detalhes = self.db.client.table("medalhas")\
            .select("*")\
            .in_("id", medalhas_ids)\
            .execute()
            
        medalhas_dict = {m["id"]: m for m in medalhas_detalhes.data}
        
        for ma in response.data:
            ma["medalha"] = medalhas_dict.get(ma["medalha_id"])
            
        return response.data

    # ==========================
    # RANKINGS
    # ==========================
    def get_ranking_geral(self, limit: int = 50) -> List[Dict[str, Any]]:
        # Utiliza a view materializada (ou view simples) criada no init_db.py
        response = self.db.client.table("ranking_geral_view")\
            .select("*")\
            .order("pontos_total", desc=True)\
            .limit(limit)\
            .execute()
        return response.data

    def get_ranking_semanal(self, limit: int = 50) -> List[Dict[str, Any]]:
        # Utiliza a função RPC criada no init_db.py
        try:
            response = self.db.client.rpc("get_ranking_semanal").execute()
            # O rpc retorna tudo, aplicamos limit em python se necessário, 
            # ou passamos limite pro rpc
            data = response.data or []
            return data[:limit]
        except Exception as e:
            logger.error(f"Erro ao buscar ranking semanal RPC: {e}")
            return []
