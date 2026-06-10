from typing import List, Optional
from fastapi import HTTPException, status
from providers.database_provider import DatabaseProvider
from repositories.mini_prova_repository import MiniProvaRepository
from repositories.tentativa_repository import TentativaRepository
from models.mini_prova import MiniProvaCreate, MiniProvaDetalhesResponse, TentativaResponse, RespostaSubmit, ResultadoTentativaResponse, RespostaResponse
from services.gamificacao_service import GamificacaoService
from services.missao_service import MissaoService
from core.constants import ACAO_MINI_PROVA_APROVADA
from datetime import datetime, timezone
import dateutil.parser

class MiniProvaService:
    def __init__(self, db: DatabaseProvider, gamificacao_service: GamificacaoService, missao_service: MissaoService):
        self.db = db
        self.repo = MiniProvaRepository(db)
        self.tentativa_repo = TentativaRepository(db)
        self.gamificacao_service = gamificacao_service
        self.missao_service = missao_service

    def criar_prova(self, professor_id: str, data: MiniProvaCreate) -> MiniProvaDetalhesResponse:
        result = self.repo.create(data, professor_id)
        return MiniProvaDetalhesResponse.model_validate(result)

    def listar_provas_turma(self, turma_id: str):
        # Aqui podemos retornar uma lista simples das provas (sem as questões detalhadas)
        # O Pydantic irá filtrar se usarmos um schema apropriado na rota
        return self.repo.list_by_turma(turma_id)

    def obter_prova_completa(self, prova_id: str) -> MiniProvaDetalhesResponse:
        prova = self.repo.get_by_id(prova_id)
        if not prova:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prova não encontrada")
        return MiniProvaDetalhesResponse.model_validate(prova)

    def iniciar_tentativa(self, aluno_id: str, mini_prova_id: str) -> TentativaResponse:
        prova = self.repo.get_by_id(mini_prova_id)
        if not prova:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prova não encontrada")

        # Verifica se o aluno pertence à turma
        turma_aluno = self.db.client.table("turma_aluno")\
            .select("*")\
            .eq("turma_id", prova["turma_id"])\
            .eq("aluno_id", aluno_id)\
            .execute()
        
        # Pode estar vazio se o módulo de turmas ainda não associou, mas vamos aplicar a regra estrita
        if not turma_aluno.data:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Aluno não pertence à turma desta prova")

        # Verifica tentativa ativa
        ativa = self.tentativa_repo.get_tentativa_ativa(aluno_id, mini_prova_id)
        if ativa:
            return TentativaResponse.model_validate(ativa)

        # Verifica tentativa já concluída (política de 1 tentativa)
        concluida = self.tentativa_repo.get_tentativa_concluida(aluno_id, mini_prova_id)
        if concluida:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Você já concluiu esta prova. Apenas uma tentativa é permitida.")

        # Cria nova tentativa (Data gerada no backend, UTC)
        nova_tentativa = self.tentativa_repo.create_tentativa(mini_prova_id, aluno_id)
        return TentativaResponse.model_validate(nova_tentativa)

    def submeter_respostas(self, aluno_id: str, tentativa_id: str, respostas: List[RespostaSubmit]) -> TentativaResponse:
        tentativa = self.tentativa_repo.get_tentativa_by_id(tentativa_id)
        if not tentativa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tentativa não encontrada")
            
        if tentativa["aluno_id"] != aluno_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tentativa pertence a outro aluno")
            
        if tentativa["concluida"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tentativa já finalizada. Múltiplas submissões não são permitidas.")

        prova = self.repo.get_by_id(tentativa["mini_prova_id"])
        
        # VALIDAÇÃO RIGOROSA DE TEMPO (Backend-Driven)
        # O Supabase retorna string ISO 8601, parseamos para datetime UTC
        data_inicio = dateutil.parser.isoparse(tentativa["data_inicio"])
        agora = datetime.now(timezone.utc)
        
        tempo_decorrido = (agora - data_inicio).total_seconds()
        
        # Adicionamos uma pequena tolerância de latência (ex: 5 segundos)
        if tempo_decorrido > (prova["tempo_limite_segundos"] + 5):
            # Se estourou, finalizamos a tentativa com nota 0 (ou a nota que daria, mas como passou, consideramos zerada/inválida)
            # Para não ser tão punitivo sem salvar nada, a regra pede erro 400. 
            # A tentativa vai ficar "pendente" para sempre ou deve ser forçada a concluir?
            # A melhor prática seria fechar ela como concluída com as respostas vazias ou zero.
            # Mas o prompt pede: "levantar HTTPException(400, 'Tempo esgotado')".
            # Vamos primeiro fechar a tentativa para não deixar o aluno tentar burlar repetidamente.
            self.tentativa_repo.finalizar_tentativa(tentativa_id, nota=0.0)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tempo esgotado")

        # CORREÇÃO AUTOMÁTICA
        nota_final = 0.0
        questoes_dict = {q["id"]: q for q in prova["questoes"]}
        
        for r in respostas:
            questao = questoes_dict.get(r.questao_id)
            if not questao:
                continue # Questão inválida, ignorar
                
            if questao["tipo"] in ["multipla_escolha", "verdadeiro_falso"]:
                # Procura a alternativa correta no gabarito
                letra_correta = None
                for alt in (questao.get("alternativas") or []):
                    if alt.get("correta") is True:
                        letra_correta = alt.get("letra")
                        break
                        
                if r.alternativa_escolhida and r.alternativa_escolhida == letra_correta:
                    nota_final += questao["pontuacao"]
            else:
                # Dissertativa: por enquanto, correção manual. Não soma pontos automaticamente.
                pass

        # Persistir respostas
        respostas_dicts = [r.model_dump() for r in respostas]
        self.tentativa_repo.registrar_respostas(tentativa_id, respostas_dicts)

        # Atualiza e finaliza a tentativa
        tentativa_atualizada = self.tentativa_repo.finalizar_tentativa(tentativa_id, nota=nota_final)
        
        # Gamificação e Missões
        pontuacao_maxima = sum([q["pontuacao"] for q in prova["questoes"]])
        nota_minima = prova.get("nota_minima_aprovacao", 0.7)
        
        # Ex: se max = 10, minima = 0.7 (70%). Aprovado se nota_final >= 7.0
        if pontuacao_maxima > 0 and (nota_final / pontuacao_maxima) >= nota_minima:
            self.gamificacao_service.conceder_pontos(aluno_id, ACAO_MINI_PROVA_APROVADA, f"Mini-Prova aprovada: {prova['id']}")
            self.missao_service.notificar_acao(aluno_id, ACAO_MINI_PROVA_APROVADA)
        
        return TentativaResponse.model_validate(tentativa_atualizada)

    def ver_resultado(self, tentativa_id: str, user_id: str, is_professor: bool) -> ResultadoTentativaResponse:
        tentativa = self.tentativa_repo.get_tentativa_by_id(tentativa_id)
        if not tentativa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tentativa não encontrada")
            
        if not is_professor and tentativa["aluno_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para ver este resultado")
            
        respostas = self.tentativa_repo.get_respostas(tentativa_id)
        prova = self.obter_prova_completa(tentativa["mini_prova_id"])
        
        return ResultadoTentativaResponse(
            tentativa=TentativaResponse.model_validate(tentativa),
            respostas=[RespostaResponse.model_validate(r) for r in respostas],
            prova=prova # Contém o gabarito (QuestaoResponse) para revisão
        )
