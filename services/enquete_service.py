from typing import List
from fastapi import HTTPException, status
from providers.database_provider import DatabaseProvider
from repositories.enquete_repository import EnqueteRepository
from models.enquete import EnqueteCreate, EnqueteResponse, VotoRequest
import logging

logger = logging.getLogger(__name__)

class EnqueteService:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.repo = EnqueteRepository(db)

    def criar_enquete(self, professor_id: str, data: EnqueteCreate) -> EnqueteResponse:
        enq_data = {
            "titulo": data.titulo,
            "descricao": data.descricao,
            "turma_id": data.turma_id,
            "professor_id": professor_id,
            "tipo": data.tipo,
            "data_fim": data.data_fim.isoformat() if data.data_fim else None
        }
        opcoes_textos = [o.texto for o in data.opcoes]
        
        result = self.repo.criar_enquete(enq_data, opcoes_textos)
        return self._formatar_resposta_com_percentuais(result)

    def get_resultado(self, enquete_id: int) -> EnqueteResponse:
        enq = self.repo.get_enquete_completa(enquete_id)
        if not enq:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Enquete não encontrada")
        return self._formatar_resposta_com_percentuais(enq)

    def listar_enquetes_turma(self, turma_id: str) -> List[EnqueteResponse]:
        enquetes = self.repo.listar_enquetes_turma(turma_id)
        # Se precisar dos percentuais na listagem, iteramos get_resultado
        # Mas para performance, podemos retornar o básico
        # Aqui, como é um payload simples, vamos só formatar os básicos (opcoes=[] no modelo base)
        return [EnqueteResponse.model_validate(e) for e in enquetes]

    def votar(self, enquete_id: int, aluno_id: str, voto: VotoRequest) -> EnqueteResponse:
        # A RPC já lida com validação de prazo, se está ativa e unicidade de voto
        # Mas podemos fazer uma checagem rápida no Python se o tipo de enquete respeita o envio de múltiplas opções
        enq = self.repo.get_enquete_completa(enquete_id)
        if not enq:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Enquete não encontrada")
            
        if enq["tipo"] == "unica" and len(voto.opcoes_ids) > 1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Esta enquete permite apenas uma opção de voto.")

        try:
            self.repo.votar(enquete_id, aluno_id, voto.opcoes_ids)
        except Exception as e:
            msg = str(e).lower()
            if "unique_violation" in msg or "votos_enquete_enquete_id_aluno_id_key" in msg:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Aluno já votou nesta enquete.")
            elif "inativa" in msg or "prazo" in msg:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Enquete encerrada ou inativa.")
            else:
                logger.error(f"Erro inesperado no voto: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Erro ao processar o voto.")

        # Retorna o resultado atualizado
        return self.get_resultado(enquete_id)

    def _formatar_resposta_com_percentuais(self, enq_dict: dict) -> EnqueteResponse:
        total_votantes = enq_dict.get("total_votantes", 0)
        
        # O cálculo de percentuais é baseado no número total de votantes únicos
        for op in enq_dict.get("opcoes", []):
            if total_votantes > 0:
                # Se for múltipla escolha, a soma dos percentuais pode ultrapassar 100%
                # pois 1 aluno pode votar em 2 opções (100% dos alunos votaram na A, 50% na B)
                op["percentual"] = round((op["contador"] / total_votantes) * 100, 2)
            else:
                op["percentual"] = 0.0
                
        return EnqueteResponse.model_validate(enq_dict)
