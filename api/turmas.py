from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from providers.database_provider import DatabaseProvider
from dependencies.auth import get_database_provider

router = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.get("/padrao", response_model=Dict[str, Any])
def get_turma_padrao(db: DatabaseProvider = Depends(get_database_provider)):
    turmas = db.fetch_all("turma", filters={"nome": "Turma Padrão MVP"})
    if not turmas:
        raise HTTPException(status_code=404, detail="Turma padrão não encontrada.")
    return turmas[0]
