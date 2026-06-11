from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider

class MockResponse:
    def __init__(self, data=None):
        self.data = data if data is not None else []

class MockQueryBuilder:
    def __init__(self, table: str, mock_client: 'MockClient'):
        self.table = table
        self.mock_client = mock_client
        self._select = "*"
        self._filters = {}
        self._limit = None
        self._order = []
        self._action = "select"
        self._action_data = None

    def select(self, columns: str):
        self._action = "select"
        self._select = columns
        return self

    def eq(self, column: str, value: Any):
        self._filters[column] = value
        return self

    def in_(self, column: str, values: List[Any]):
        self._filters[column] = {"$in": values}
        return self

    def lte(self, column: str, value: Any):
        self._filters[column] = {"$lte": value}
        return self

    def order(self, column: str, desc: bool = False):
        self._order.append((column, desc))
        return self

    def is_(self, column: str, value: Any):
        if value == "null":
            self._filters[column] = None
        else:
            self._filters[column] = value
        return self
        
    def or_(self, condition: str):
        # Simplificando or_ para testes (apenas dummy)
        return self

    def limit(self, limit: int):
        self._limit = limit
        return self

    def insert(self, data: Any):
        self._action = "insert"
        self._action_data = data
        return self

    def update(self, data: Dict[str, Any]):
        self._action = "update"
        self._action_data = data
        return self

    def delete(self):
        self._action = "delete"
        return self

    def execute(self):
        if self.mock_client.should_error:
            raise Exception(f"Mock error: {self._action} failed")

        if self._action == "insert":
            if self.table not in self.mock_client.data_store:
                self.mock_client.data_store[self.table] = []
                
            data = self._action_data
            import uuid
            if isinstance(data, list):
                for item in data:
                    if "id" not in item:
                        item["id"] = str(uuid.uuid4())
                    item.setdefault("nivel_atual", 1)
                    item.setdefault("xp_acumulado", 0)
                    item.setdefault("criado_em", "2026-01-01T00:00:00Z")
                    item.setdefault("data_criacao", "2026-01-01T00:00:00Z")
                    item.setdefault("medalhas", [])
                self.mock_client.data_store[self.table].extend(data)
                return MockResponse(data=data)
            else:
                if "id" not in data:
                    data["id"] = str(uuid.uuid4())
                data.setdefault("nivel_atual", 1)
                data.setdefault("xp_acumulado", 0)
                data.setdefault("criado_em", "2026-01-01T00:00:00Z")
                data.setdefault("data_criacao", "2026-01-01T00:00:00Z")
                data.setdefault("medalhas", [])
                self.mock_client.data_store[self.table].append(data)
                return MockResponse(data=[data])

        elif self._action == "update":
            updated = []
            table_data = self.mock_client.data_store.get(self.table, [])
            for row in table_data:
                match = True
                for k, v in self._filters.items():
                    if row.get(k) != v:
                        match = False
                if match:
                    row.update(self._action_data)
                    updated.append(row)
            return MockResponse(data=updated)

        elif self._action == "delete":
            table_data = self.mock_client.data_store.get(self.table, [])
            new_data = []
            for row in table_data:
                match = True
                for k, v in self._filters.items():
                    if row.get(k) != v:
                        match = False
                if not match:
                    new_data.append(row)
            self.mock_client.data_store[self.table] = new_data
            return MockResponse(data=[])

        elif self._action == "select":
            results = []
            table_data = self.mock_client.data_store.get(self.table, [])
            for row in table_data:
                match = True
                for k, v in self._filters.items():
                    if isinstance(v, dict) and "$in" in v:
                        if row.get(k) not in v["$in"]:
                            match = False
                    elif isinstance(v, dict) and "$lte" in v:
                        if row.get(k) > v["$lte"]:
                            match = False
                    else:
                        if row.get(k) != v:
                            match = False
                if match:
                    results.append(row)
                    
            if self._order:
                for col, desc in reversed(self._order):
                    results.sort(key=lambda x: x.get(col, 0) if x.get(col) is not None else 0, reverse=desc)
                    
            if self._limit:
                results = results[:self._limit]
                
            return MockResponse(data=results)

class MockClient:
    def __init__(self):
        self.data_store: Dict[str, List[Dict[str, Any]]] = {}
        self.should_error = False
        self.rpc_store = {}

    def table(self, table_name: str) -> MockQueryBuilder:
        return MockQueryBuilder(table_name, self)
        
    def rpc(self, func_name: str, **kwargs):
        class RpcResponse:
            def execute(self_rpc):
                if self.should_error:
                    raise Exception("Mock error: rpc failed")
                return MockResponse(data=self.rpc_store.get(func_name, []))
        return RpcResponse()

class MockProvider(DatabaseProvider):
    def __init__(self):
        self.client = MockClient()

    def fetch_all(self, table: str, filters: Optional[Dict[str, Any]] = None, columns: str = "*", order_by: Optional[str] = None, order_desc: bool = False, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = self.client.table(table).select(columns)
        if filters:
            for k, v in filters.items():
                query = query.eq(k, v)
        if order_by:
            query = query.order(order_by, desc=order_desc)
        if limit:
            query = query.limit(limit)
        return query.execute().data

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
