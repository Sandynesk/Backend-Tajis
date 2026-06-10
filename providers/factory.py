from typing import Dict, Type
from providers.database_provider import DatabaseProvider
from providers.supabase_provider import SupabaseProvider

class ProviderFactory:
    """
    Fábrica para instanciar estratégias de persistência de dados (Provider Pattern).
    """
    _registry: Dict[str, Type[DatabaseProvider]] = {
        "supabase": SupabaseProvider,
        "sql": SupabaseProvider, # Aponta para Supabase por padrão, podendo ser mapeado para outros no futuro
    }

    @classmethod
    def register(cls, name: str, provider_cls: Type[DatabaseProvider]):
        """
        Permite registrar novas estratégias de banco de dados dinamicamente.
        """
        cls._registry[name.lower()] = provider_cls

    @classmethod
    def create(cls, name: str = "supabase", *args, **kwargs) -> DatabaseProvider:
        """
        Instancia e retorna o provedor de banco de dados correspondente.
        """
        provider_cls = cls._registry.get(name.lower())
        if not provider_cls:
            raise ValueError(
                f"Provedor de banco de dados '{name}' não registrado. "
                f"Opções disponíveis: {list(cls._registry.keys())}"
            )
        return provider_cls(*args, **kwargs)
