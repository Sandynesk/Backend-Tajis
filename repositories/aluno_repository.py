from typing import Optional, Dict, Any
from providers.database_provider import DatabaseProvider

class AlunoRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.table_name = "aluno"

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        results = self.db.fetch_all(self.table_name, filters={"email": email}, limit=1)
        return results[0] if results else None

    def get_by_id(self, aluno_id: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_by_id(self.table_name, id_value=aluno_id)

    def create(self, aluno_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.db.insert(self.table_name, aluno_data)
