# Camada Models (Entidades e Schemas)

## Responsabilidade
Centraliza a definição de todas as estruturas de dados do sistema:
1. **Entidades do Banco (Models):** Representam as tabelas e colunas físicas do banco de dados relacional.
2. **Schemas Pydantic (Validação):** Estruturas de dados para validação de requisições de entrada (Request Payloads) e respostas de saída (Response Schemas) da API.

## Regras
- Devem ser puramente declarativos (sem regras de negócio).
- Servem como contrato de tipo entre o banco de dados, o backend e a API.

## Arquivos e Módulos
- **`desafio.py`**: Modelos e Schemas para Desafios e Submissões de alunos.
- **`disciplina.py`**: Modelos para Disciplinas/Matérias do sistema educacional.
- **`enquete.py`**: Modelos para as Enquetes, Opções de Resposta e Votos computados.
- **`formacao.py`**: Modelos e schemas que representam a Formação de Equipes e seus Grupos.
- **`gamificacao.py`**: Estruturas de dados para o sistema gamificado (Ranking, XP, Níveis, Histórico de Pontos e Medalhas).
- **`mini_prova.py`**: Modelos completos e complexos das Avaliações temporizadas, abrangendo a Prova em si, as Questões, as Alternativas e as Tentativas e Respostas do Aluno.
- **`missao.py`**: Modelos das Missões educacionais (trilhas), suas Etapas individuais e o Progresso do Aluno na missão.
- **`turma.py`**: Modelos que definem as Turmas e o vínculo dos Professores.
- **`user.py`**: Modelos base para usuários, cobrindo as identidades de Alunos e Professores.
