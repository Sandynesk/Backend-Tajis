from typing import List, Optional
from fastapi import HTTPException, status
from providers.database_provider import DatabaseProvider
from repositories.gamificacao_repository import GamificacaoRepository
from models.gamificacao import RankingEntry, NivelResponse, MedalhaAlunoResponse, PontuacaoResponse
import logging

logger = logging.getLogger(__name__)

class GamificacaoService:
    def __init__(self, db: DatabaseProvider):
        self.db = db
        self.repo = GamificacaoRepository(db)

    def conceder_pontos(self, aluno_id: str, acao_nome: str, descricao: Optional[str] = None):
        """
        Registra pontos para um aluno com base em uma ação.
        Após conceder, verifica a possibilidade de novas medalhas.
        """
        try:
            pontuacao = self.repo.registrar_pontuacao(aluno_id, acao_nome, descricao)
            if pontuacao:
                logger.info(f"Concedido {pontuacao['pontos_ganhos']} pontos para aluno {aluno_id} (Ação: {acao_nome})")
                self.conceder_medalhas_automaticas(aluno_id)
        except Exception as e:
            # Opção B: Falha na transação compensada via log. Não bloqueia a requisição principal.
            logger.error(f"Erro ao conceder pontos para {aluno_id} (Ação: {acao_nome}): {e}")

    def verificar_nivel(self, aluno_id: str) -> Optional[NivelResponse]:
        """
        Calcula dinamicamente o nível do aluno com base no seu total de pontos.
        Para evitar tabelas inconsistentes, o nível não fica gravado em "alunos".
        """
        # Obter pontos totais
        # O Ranking geral traz o total calculado. Podemos usá-lo ou fazer uma query rápida.
        # Mas para o perfil individual, vamos pegar da view de ranking ou calcular:
        response = self.db.client.table("ranking_geral_view")\
            .select("pontos_total")\
            .eq("aluno_id", aluno_id)\
            .execute()
            
        pontos_total = response.data[0]["pontos_total"] if response.data else 0
        
        nivel_data = self.repo.get_nivel_por_pontos(pontos_total)
        if nivel_data:
            return NivelResponse.model_validate(nivel_data)
        return None

    def conceder_medalhas_automaticas(self, aluno_id: str):
        """
        Avalia o histórico do aluno e concede medalhas baseadas em critérios hardcoded ou dinâmicos.
        O repositório já ignora duplicatas de forma graciosa.
        """
        # Exemplo simples: vamos buscar todas as medalhas e ver se ele atende o critério.
        medalhas_db = self.db.client.table("medalhas").select("*").execute()
        historico = self.repo.get_historico_pontos(aluno_id)
        
        # Mapear as ações realizadas
        acoes_realizadas = set()
        for p in historico:
            # Para otimizar, o ideal é o repositório retornar o NOME da ação no histórico.
            # Aqui vamos assumir que o critério possa ser o nome da ação.
            # Em MVP, daremos medalha pelo ID da ação (ex: 1 = primeiro desafio)
            acoes_realizadas.add(p["acao_id"])
            
        # Para fins de MVP, vamos simplificar:
        # Se a medalha tem como 'criterio' o nome da ação.
        # Como não temos o join das ações aqui facilmente, faremos uma verificação genérica:
        acoes_db = self.db.client.table("acoes_gamificacao").select("*").execute()
        acoes_dict = {a["id"]: a["nome"] for a in acoes_db.data}
        
        nomes_acoes_realizadas = {acoes_dict.get(aid) for aid in acoes_realizadas if acoes_dict.get(aid)}
        
        for medalha in medalhas_db.data:
            criterio = medalha["criterio"] # ex: "desafio_concluido"
            if criterio in nomes_acoes_realizadas:
                self.repo.conceder_medalha(aluno_id, medalha["id"])

    def obter_ranking_geral(self) -> List[RankingEntry]:
        dados = self.repo.get_ranking_geral()
        ranking = []
        for i, d in enumerate(dados):
            nivel = self.repo.get_nivel_por_pontos(d["pontos_total"])
            
            entry = RankingEntry(
                posicao=i + 1,
                aluno_id=d["aluno_id"],
                nome_aluno=d["nome_aluno"],
                pontos_total=d["pontos_total"],
                nivel_atual=nivel["nome"] if nivel else "Iniciante",
                medalhas=d["medalhas"]
            )
            ranking.append(entry)
        return ranking

    def obter_ranking_semanal(self) -> List[RankingEntry]:
        dados = self.repo.get_ranking_semanal()
        ranking = []
        for i, d in enumerate(dados):
            # No semanal, podemos ou não retornar o nível global, vamos retornar
            nivel = self.repo.get_nivel_por_pontos(d["pontos_total"])
            entry = RankingEntry(
                posicao=i + 1,
                aluno_id=d["aluno_id"],
                nome_aluno=d["nome_aluno"],
                pontos_total=d["pontos_total"],
                nivel_atual=nivel["nome"] if nivel else "Iniciante",
                medalhas=d["medalhas"]
            )
            ranking.append(entry)
        return ranking

    def listar_medalhas_aluno(self, aluno_id: str) -> List[MedalhaAlunoResponse]:
        medalhas = self.repo.get_medalhas_aluno(aluno_id)
        return [MedalhaAlunoResponse.model_validate(m) for m in medalhas]
        
    def listar_historico_pontos(self, aluno_id: str) -> List[PontuacaoResponse]:
        historico = self.repo.get_historico_pontos(aluno_id)
        return [PontuacaoResponse.model_validate(h) for h in historico]
