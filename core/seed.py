from providers import ProviderFactory
import logging

logger = logging.getLogger(__name__)

async def run_seed():
    """Garante que a Disciplina e Turma Padrão do MVP existam no banco."""
    db = ProviderFactory.create("supabase")
    
    # 1. Checar se a disciplina padrão existe (buscando pelo código)
    disciplinas = db.fetch_all("disciplina", filters={"codigo": "DISC-MVP"})
    if not disciplinas:
        logger.info("Criando Disciplina Padrão do MVP...")
        disciplina = db.insert("disciplina", {
            "nome": "Disciplina Base MVP",
            "codigo": "DISC-MVP"
        })
        disciplina_id = disciplina.get("id")
    else:
        disciplina_id = disciplinas[0].get("id")

    # 2. Checar se a turma padrão existe
    turmas = db.fetch_all("turma", filters={"nome": "Turma Padrão MVP"})
    if not turmas:
        logger.info("Criando Turma Padrão do MVP...")
        db.insert("turma", {
            "nome": "Turma Padrão MVP",
            "disciplina_id": disciplina_id
        })
        logger.info("Seed concluído com sucesso!")
    else:
        logger.info("Turma Padrão já existe. Nenhuma ação necessária.")
