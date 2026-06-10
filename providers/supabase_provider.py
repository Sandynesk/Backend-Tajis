from typing import List, Dict, Any, Optional
from database import supabase
from providers.database_provider import DatabaseProvider

class SupabaseProvider(DatabaseProvider):
    """
    Implementação concreta do DatabaseProvider usando o cliente do Supabase.
    """

    def __init__(self, client=None):
        # Permite injeção de dependência para facilidade de testes, senão usa a instância padrão
        self.client = client or supabase

    def fetch_all(
        self, 
        table: str, 
        filters: Optional[Dict[str, Any]] = None,
        columns: str = "*",
        order_by: Optional[str] = None,
        order_desc: bool = False,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        query = self.client.table(table).select(columns)
        
        if filters:
            for key, val in filters.items():
                query = query.eq(key, val)
                
        if order_by:
            query = query.order(order_by, desc=order_desc)
            
        if limit is not None:
            query = query.limit(limit)
            
        response = query.execute()
        return response.data

    def fetch_by_id(self, table: str, id_value: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        response = self.client.table(table).select("*").eq(id_column, id_value).execute()
        return response.data[0] if response.data else None

    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table(table).insert(data).execute()
        return response.data[0] if response.data else response.data

    def update(self, table: str, id_value: Any, data: Dict[str, Any], id_column: str = "id") -> Dict[str, Any]:
        response = self.client.table(table).update(data).eq(id_column, id_value).execute()
        return response.data[0] if response.data else response.data

    def delete(self, table: str, id_value: Any, id_column: str = "id") -> bool:
        self.client.table(table).delete().eq(id_column, id_value).execute()
        return True
