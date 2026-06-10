from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Projeto Integrador - Plataforma Educacional",
    description="Backend para plataforma baseada em metodologias ativas.",
    version="0.1.0"
)

# Configuração de CORS (importante para integração com Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api import auth, desafios, mini_provas, gamificacao, missoes, formacao, enquetes
from core.init_db import init_db

app.include_router(auth.router)
app.include_router(desafios.router)
app.include_router(mini_provas.router)
app.include_router(gamificacao.router)
app.include_router(missoes.router)
app.include_router(formacao.router)
app.include_router(enquetes.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Backend do Projeto Integrador ativo. Acesse /docs para documentação OpenAPI."
    }
