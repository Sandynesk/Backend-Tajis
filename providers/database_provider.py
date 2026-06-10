from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DatabaseProvider(ABC):
    """
    Interface base que define o contrato para estratégias de persistência de dados.
    Esta interface garante o desacoplamento entre a regra de negócio e o banco de dados.
    """

    @abstractmethod
    def fetch_all(
        self, 
        table: str, 
        filters: Optional[Dict[str, Any]] = None,
        columns: str = "*",
        order_by: Optional[str] = None,
        order_desc: bool = False,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca todos os registros de uma tabela que atendam aos filtros opcionais.
        """
        pass

    @abstractmethod
    def fetch_by_id(self, table: str, id_value: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        """
        Busca um único registro na tabela pelo seu identificador (ID).
        """
        pass

    @abstractmethod
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insere um novo registro na tabela.
        """
        pass

    @abstractmethod
    def update(self, table: str, id_value: Any, data: Dict[str, Any], id_column: str = "id") -> Dict[str, Any]:
        """
        Atualiza um registro existente na tabela filtrado pelo ID.
        """
        pass

    @abstractmethod
    def delete(self, table: str, id_value: Any, id_column: str = "id") -> bool:
        """
        Remove um registro da tabela filtrado pelo ID.
        """
        pass
