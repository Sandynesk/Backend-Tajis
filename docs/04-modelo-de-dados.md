# Modelo de Dados e Entidades Sugeridas

Abaixo estão as entidades primárias identificadas e separadas por contexto. 
No banco de dados relacional (Supabase), estas representarão as tabelas, enquanto no backend (FastAPI), representarão as Models/Schemas (`models/`).

## Entidades Globais
- **Aluno:** (Ex: `id`, `nome`, `email`, `senha_hash`, `criado_em`)
- **Professor:** (Ex: `id`, `nome`, `email`, `senha_hash`, `departamento`)
- **Disciplina:** (Ex: `id`, `nome`, `codigo`)
- **Turma:** (Ex: `id`, `nome`, `disciplina_id`, `professor_id`)
- **Pontuação:** (Tabela de apoio genérica ou histórico)

## Contexto: Sistema de Desafios
- `desafio`: Dados do problema proposto (título, descrição, prazo, disciplina_id).
- `submissao`: A resposta submetida pelo aluno.
- `voto`: Avaliação da submissão (se aplicável ao tipo de desafio).
- `nota`: Nota consolidada após correção ou votação.
- `ranking`: Agregação pontual para visualização no dashboard.

## Contexto: Mini-Provas
- `prova`: Cabeçalho da avaliação.
- `questao`: Questões vinculadas à prova.
- `tentativa`: Registro de que um aluno iniciou a prova (crucial para controlar o cronômetro de 5 minutos).
- `resposta`: Opção assinalada pelo aluno por questão.
- `pontuacao`: Nota final salva após a correção automática.

## Contexto: Gamificação
- `medalha`: Dicionário/catálogo de medalhas existentes.
- `conquista`: Associação de qual aluno ganhou qual medalha.
- `nivel`: Definição da tabela de experiência/XP por nível.
- `historico_pontos`: Log de transações de entrada de pontos (ex: "+10 pontos por completar prova Y").
- `ranking`: View ou tabela materializada agrupando o histórico_pontos.

## Contexto: Feedback Instantâneo
- `enquete`: Pergunta rápida gerada.
- `pergunta`: Caso a enquete tenha múltiplas perguntas.
- `resposta`: Feedback rápido do aluno.
- `estatistica`: Resultado computado.

## Contexto: Formação de Equipes
- `equipe`: O grupo gerado.
- `integrante`: Tabela de ligação aluno <-> equipe.
- `habilidade`: Tags ou skills de um aluno.
- `criterio`: Regras configuradas pelo professor para o gerador.

## Contexto: Missões Educacionais
- `missao`: A jornada principal.
- `etapa`: Passos dentro da missão.
- `progresso`: Estado atual do aluno na missão.
- `recompensa`: Prêmio ao concluir a missão/etapa.
