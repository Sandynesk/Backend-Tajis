# Pacote para o Provider Pattern (Estratégias de persistência de dados)
from .database_provider import DatabaseProvider
from .supabase_provider import SupabaseProvider
from .factory import ProviderFactory

__all__ = ["DatabaseProvider", "SupabaseProvider", "ProviderFactory"]
