from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
from models.desafio import DesafioCreate, DesafioAlunoUpdate
from datetime import datetime

class DesafioRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.table_desafios = "desafios"
        self.table_alunos = "desafios_alunos"

    def create(self, desafio: DesafioCreate, professor_id: str) -> Dict[str, Any]:
        data = desafio.model_dump()
        data["professor_id"] = professor_id
        return self.db.insert(self.table_desafios, data)

    def list_by_turma(self, turma_id: str) -> List[Dict[str, Any]]:
        return self.db.fetch_all(self.table_desafios, filters={"turma_id": turma_id})

    def assign_to_aluno(self, desafio_id: str, aluno_id: str) -> Dict[str, Any]:
        data = {
            "desafio_id": desafio_id,
            "aluno_id": aluno_id,
            "status": "pendente"
        }
        return self.db.insert(self.table_alunos, data)

    def update_status(self, desafio_id: str, aluno_id: str, data: DesafioAlunoUpdate) -> Optional[Dict[str, Any]]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return None
            
        if update_data.get("status") == "concluido" and "data_conclusao" not in update_data:
            update_data["data_conclusao"] = datetime.utcnow().isoformat()
            
        response = self.db.client.table(self.table_alunos)\
            .update(update_data)\
            .eq("desafio_id", desafio_id)\
            .eq("aluno_id", aluno_id)\
            .execute()
            
        return response.data[0] if response.data else None

    def get_aluno_desafios(self, aluno_id: str) -> List[Dict[str, Any]]:
        return self.db.fetch_all(self.table_alunos, filters={"aluno_id": aluno_id})
        
    def get_by_id(self, desafio_id: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_by_id(self.table_desafios, id_value=desafio_id)

    def get_atribuicao(self, desafio_id: str, aluno_id: str) -> Optional[Dict[str, Any]]:
        response = self.db.client.table(self.table_alunos)\
            .select("*")\
            .eq("desafio_id", desafio_id)\
            .eq("aluno_id", aluno_id)\
            .execute()
        return response.data[0] if response.data else None
