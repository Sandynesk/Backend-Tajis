from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Projeto Integrador Backend TAJI"
    
    # Segurança
    SECRET_KEY: str = "sua_chave_secreta_super_segura_para_desenvolvimento_aqui"  # Em produção, mudar no .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias para facilitar o desenvolvimento
    
    # Banco de Dados
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
