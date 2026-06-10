import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("Variáveis de ambiente SUPABASE_URL e SUPABASE_ANON_KEY devem estar definidas no arquivo .env")

supabase: Client = create_client(url, key)
