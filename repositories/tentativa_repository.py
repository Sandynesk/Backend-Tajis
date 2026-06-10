from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class TentativaRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.table_tentativas = "tentativas"
        self.table_respostas = "respostas"

    def create_tentativa(self, mini_prova_id: str, aluno_id: str) -> Dict[str, Any]:
        """
        Cria uma nova tentativa com a data_inicio gerada no backend em UTC.
        Nunca aceita data do cliente.
        """
        data = {
            "mini_prova_id": mini_prova_id,
            "aluno_id": aluno_id,
            "data_inicio": datetime.now(timezone.utc).isoformat(),
            "concluida": False
        }
        return self.db.insert(self.table_tentativas, data)

    def get_tentativa_by_id(self, tentativa_id: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_by_id(self.table_tentativas, id_value=tentativa_id)

    def get_tentativa_ativa(self, aluno_id: str, mini_prova_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca uma tentativa não concluída para o aluno e prova especificados.
        """
        response = self.db.client.table(self.table_tentativas)\
            .select("*")\
            .eq("aluno_id", aluno_id)\
            .eq("mini_prova_id", mini_prova_id)\
            .eq("concluida", False)\
            .execute()
        return response.data[0] if response.data else None
        
    def get_tentativa_concluida(self, aluno_id: str, mini_prova_id: str) -> Optional[Dict[str, Any]]:
        """
        Verifica se já existe alguma tentativa concluída para bloquear novas tentativas
        (se a política for de 1 tentativa apenas).
        """
        response = self.db.client.table(self.table_tentativas)\
            .select("*")\
            .eq("aluno_id", aluno_id)\
            .eq("mini_prova_id", mini_prova_id)\
            .eq("concluida", True)\
            .execute()
        return response.data[0] if response.data else None

    def finalizar_tentativa(self, tentativa_id: str, nota: float) -> Dict[str, Any]:
        data = {
            "data_fim": datetime.now(timezone.utc).isoformat(),
            "nota_final": nota,
            "concluida": True
        }
        return self.db.update(self.table_tentativas, id_value=tentativa_id, data=data)

    def registrar_respostas(self, tentativa_id: str, respostas_dicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Insere múltiplas respostas de uma vez.
        O Supabase (PostgREST) aceita array de objetos no insert.
        """
        if not respostas_dicts:
            return []
            
        for r in respostas_dicts:
            r["tentativa_id"] = tentativa_id
            
        response = self.db.client.table(self.table_respostas).insert(respostas_dicts).execute()
        return response.data
        
    def get_respostas(self, tentativa_id: str) -> List[Dict[str, Any]]:
        return self.db.fetch_all(self.table_respostas, filters={"tentativa_id": tentativa_id})
