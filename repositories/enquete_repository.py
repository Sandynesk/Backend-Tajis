from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
import logging

logger = logging.getLogger(__name__)

class EnqueteRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    def criar_enquete(self, enquete_data: Dict[str, Any], opcoes_textos: List[str]) -> Optional[Dict[str, Any]]:
        try:
            enq = self.db.insert("enquetes", enquete_data)
            enquete_id = enq["id"]
            
            for texto in opcoes_textos:
                self.db.insert("opcoes_enquete", {
                    "enquete_id": enquete_id,
                    "texto": texto
                })
            return self.get_enquete_completa(enquete_id)
        except Exception as e:
            logger.error(f"Erro ao criar enquete: {e}")
            raise e

    def get_enquete_completa(self, enquete_id: int) -> Optional[Dict[str, Any]]:
        res_enq = self.db.client.table("enquetes").select("*").eq("id", enquete_id).execute()
        if not res_enq.data:
            return None
        enquete = res_enq.data[0]
        
        res_opc = self.db.client.table("opcoes_enquete").select("*").eq("enquete_id", enquete_id).order("id").execute()
        enquete["opcoes"] = res_opc.data
        
        # Obter o total de alunos que votaram para calcular percentuais depois
        # Uma forma de fazer isso é contando a tabela votos_enquete
        res_votos = self.db.client.table("votos_enquete").select("id", count="exact").eq("enquete_id", enquete_id).execute()
        enquete["total_votantes"] = res_votos.count if res_votos.count else 0
        
        return enquete

    def listar_enquetes_turma(self, turma_id: str) -> List[Dict[str, Any]]:
        res = self.db.client.table("enquetes").select("*").eq("turma_id", turma_id).order("data_criacao", desc=True).execute()
        return res.data

    def votar(self, enquete_id: int, aluno_id: str, opcoes_ids: List[int]) -> bool:
        """ Executa o voto através da RPC atômica """
        try:
            # O PostgreSQL array mapeia para lista no supabase-py / python
            self.db.client.rpc(
                "registrar_voto_enquete",
                {
                    "p_enquete_id": enquete_id,
                    "p_aluno_id": aluno_id,
                    "p_opcoes_ids": opcoes_ids
                }
            ).execute()
            return True
        except Exception as e:
            # Erros de validação da RPC, como 'Aluno já votou' ou 'Opção inválida', caem aqui.
            logger.error(f"Erro ao registrar voto na enquete {enquete_id}: {e}")
            raise e
