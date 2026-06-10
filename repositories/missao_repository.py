from typing import List, Dict, Any, Optional
from providers.database_provider import DatabaseProvider
from models.missao import MissaoCreate
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class MissaoRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    def create(self, missao_data: MissaoCreate, professor_id: str) -> Dict[str, Any]:
        """
        Cria a missão e suas etapas sequencialmente (compensação em caso de erro).
        """
        m_dict = {
            "titulo": missao_data.titulo,
            "descricao": missao_data.descricao,
            "professor_id": professor_id,
            "turma_id": missao_data.turma_id,
            "tipo": missao_data.tipo,
            "pontos_recompensa": missao_data.pontos_recompensa
        }
        
        missao_inserida = self.db.insert("missoes", m_dict)
        missao_id = missao_inserida["id"]
        
        try:
            etapas_inseridas = []
            for etapa in missao_data.etapas:
                e_dict = {
                    "missao_id": missao_id,
                    "ordem": etapa.ordem,
                    "descricao": etapa.descricao,
                    "tipo_acao": etapa.tipo_acao,
                    "meta": etapa.meta,
                    "pontos_etapa": etapa.pontos_etapa
                }
                e_ins = self.db.insert("etapas_missao", e_dict)
                etapas_inseridas.append(e_ins)
                
            missao_inserida["etapas"] = etapas_inseridas
            return missao_inserida
        except Exception as e:
            logger.error(f"Erro ao inserir etapas da missão {missao_id}. Rollback manual. Erro: {e}")
            self.db.delete("missoes", missao_id)
            raise e

    def get_by_id(self, missao_id: int) -> Optional[Dict[str, Any]]:
        missao = self.db.fetch_by_id("missoes", missao_id)
        if not missao:
            return None
        etapas = self.db.fetch_all("etapas_missao", filters={"missao_id": missao_id}, order_by="ordem")
        missao["etapas"] = etapas
        return missao

    def list_disponiveis(self, turma_id: Optional[str] = None) -> List[Dict[str, Any]]:
        # Filtra missões globais (turma nula) ou da turma específica
        query = self.db.client.table("missoes").select("*").eq("ativa", True)
        if turma_id:
            query = query.or_(f"turma_id.eq.{turma_id},turma_id.is.null")
        else:
            query = query.is_("turma_id", "null")
            
        response = query.execute()
        return response.data

class ProgressoMissaoRepository:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    def get_progresso(self, aluno_id: str, missao_id: int) -> Optional[Dict[str, Any]]:
        res = self.db.client.table("progresso_missao")\
            .select("*")\
            .eq("aluno_id", aluno_id)\
            .eq("missao_id", missao_id)\
            .execute()
        if not res.data:
            return None
            
        progresso = res.data[0]
        # Carregar progresso das etapas
        etapas_prog = self.db.client.table("progresso_etapa")\
            .select("*")\
            .eq("progresso_id", progresso["id"])\
            .execute()
            
        progresso["etapas_progresso"] = etapas_prog.data
        return progresso

    def iniciar_missao(self, aluno_id: str, missao_id: int, etapas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """ Inicia progresso da missão e cria registros de progresso para cada etapa com contador 0 """
        p_dict = {
            "aluno_id": aluno_id,
            "missao_id": missao_id,
            "etapa_atual": 1,
            "concluida": False,
            "data_inicio": datetime.now(timezone.utc).isoformat()
        }
        progresso = self.db.insert("progresso_missao", p_dict)
        prog_id = progresso["id"]
        
        try:
            p_etapas = []
            for etapa in etapas:
                pe_dict = {
                    "progresso_id": prog_id,
                    "etapa_id": etapa["id"],
                    "contador": 0,
                    "concluida": False
                }
                pe_ins = self.db.insert("progresso_etapa", pe_dict)
                p_etapas.append(pe_ins)
            
            progresso["etapas_progresso"] = p_etapas
            return progresso
        except Exception as e:
            logger.error(f"Erro ao iniciar progresso da missão {missao_id}. Rollback. Erro: {e}")
            self.db.delete("progresso_missao", prog_id)
            raise e

    def get_missoes_em_andamento(self, aluno_id: str) -> List[Dict[str, Any]]:
        res = self.db.client.table("progresso_missao")\
            .select("*")\
            .eq("aluno_id", aluno_id)\
            .eq("concluida", False)\
            .execute()
        return res.data

    def get_progresso_etapa(self, progresso_id: int, etapa_id: int) -> Optional[Dict[str, Any]]:
        res = self.db.client.table("progresso_etapa")\
            .select("*")\
            .eq("progresso_id", progresso_id)\
            .eq("etapa_id", etapa_id)\
            .execute()
        return res.data[0] if res.data else None

    def atualizar_contador_etapa(self, progresso_etapa_id: int, novo_contador: int, concluida: bool) -> Dict[str, Any]:
        return self.db.update("progresso_etapa", progresso_etapa_id, {
            "contador": novo_contador,
            "concluida": concluida
        })

    def avancar_etapa_missao(self, progresso_id: int, nova_etapa_atual: int) -> Dict[str, Any]:
        return self.db.update("progresso_missao", progresso_id, {"etapa_atual": nova_etapa_atual})

    def concluir_missao(self, progresso_id: int) -> Dict[str, Any]:
        return self.db.update("progresso_missao", progresso_id, {
            "concluida": True,
            "data_conclusao": datetime.now(timezone.utc).isoformat()
        })
