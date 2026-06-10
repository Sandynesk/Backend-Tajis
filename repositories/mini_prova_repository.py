from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
from models.mini_prova import MiniProvaCreate
import logging

logger = logging.getLogger(__name__)

class MiniProvaRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.table_provas = "mini_provas"
        self.table_questoes = "questoes"

    def create(self, prova_data: MiniProvaCreate, professor_id: str) -> Dict[str, Any]:
        """
        Cria a prova e suas questões sequencialmente.
        Em caso de falha nas questões, realiza o rollback (compensação) removendo a prova.
        """
        # Extrai os dados da prova (sem as questões)
        prova_dict = {
            "titulo": prova_data.titulo,
            "descricao": prova_data.descricao,
            "turma_id": prova_data.turma_id,
            "tempo_limite_segundos": prova_data.tempo_limite_segundos,
            "nota_minima_aprovacao": prova_data.nota_minima_aprovacao,
            "professor_id": professor_id
        }
        
        # Insere a prova
        prova_inserida = self.db.insert(self.table_provas, prova_dict)
        prova_id = prova_inserida["id"]
        
        # Tenta inserir as questões
        try:
            questoes_inseridas = []
            for questao in prova_data.questoes:
                questao_dict = {
                    "mini_prova_id": prova_id,
                    "enunciado": questao.enunciado,
                    "tipo": questao.tipo,
                    "pontuacao": questao.pontuacao,
                    # alternativas como lista de dicts (já vem serializado pelo model_dump se tratarmos)
                    "alternativas": [alt.model_dump() for alt in questao.alternativas] if questao.alternativas else None
                }
                q_inserida = self.db.insert(self.table_questoes, questao_dict)
                questoes_inseridas.append(q_inserida)
                
            prova_inserida["questoes"] = questoes_inseridas
            return prova_inserida
            
        except Exception as e:
            # Compensação (Rollback)
            logger.error(f"Erro ao inserir questões da prova {prova_id}. Realizando rollback. Erro: {e}")
            self.db.delete(self.table_provas, id_value=prova_id)
            raise e

    def get_by_id(self, mini_prova_id: str) -> Optional[Dict[str, Any]]:
        prova = self.db.fetch_by_id(self.table_provas, id_value=mini_prova_id)
        if not prova:
            return None
            
        questoes = self.db.fetch_all(self.table_questoes, filters={"mini_prova_id": mini_prova_id})
        prova["questoes"] = questoes
        return prova

    def list_by_turma(self, turma_id: str) -> List[Dict[str, Any]]:
        return self.db.fetch_all(self.table_provas, filters={"turma_id": turma_id})
