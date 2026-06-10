# Camada Repositories (Acesso aos Dados)

## Responsabilidade
Funciona como um intermediário entre a camada de regras de negócio (`services/`) e a infraestrutura de banco de dados (`providers/`). Ela define como os dados são obtidos e salvos.

## Regras
- Interage diretamente com a camada de `providers` (que por sua vez interage com o banco de dados Supabase/SQL).
- Centraliza operações de CRUD (Create, Read, Update, Delete) de entidades específicas (ex: `AlunoRepository`).
- Permite que a camada de serviços obtenha entidades limpas sem precisar saber como o SQL ou o banco de dados está estruturado.

## Arquivos e Módulos
- **`aluno_repository.py`**: Interações de banco de dados envolvendo os usuários do tipo Aluno (consultas de e-mail e criação).
- **`professor_repository.py`**: Interações de banco de dados envolvendo usuários do tipo Professor.
- **`desafio_repository.py`**: Manipula operações relacionadas ao módulo de desafios, incluindo criação e deleção no banco.
- **`enquete_repository.py`**: Repositório focado na persistência e manipulação de enquetes criadas e do cômputo de votos.
- **`formacao_repository.py`**: Executa chamadas no banco referentes à formação de equipes e armazenamento de grupos de alunos.
- **`gamificacao_repository.py`**: Interage com a infraestrutura de banco para obter ranking global, registrar medalhas, aumentar o progresso de XP do aluno.
- **`mini_prova_repository.py`**: Recupera e injeta registros das avaliações de tempo limitado, além de validar os limites por turma.
- **`missao_repository.py`**: Persiste as definições complexas das Trilhas de Missões, incluindo as etapas vinculadas a cada uma.
- **`tentativa_repository.py`**: Repositório isolado para lidar especificamente com a submissão de respostas e tentativas das mini-provas, processando e comparando respostas e acionando RPCs para cálculo de nota.
