# Camada Services (Regras de Negócio)

## Responsabilidade
É o coração do backend. Contém toda a lógica de negócio do sistema (cálculo de médias, validação de regras de tempo para mini-provas, processamento de gamificação e pontos, algoritmo de distribuição de equipes).

## Regras
- **Não** sabe nada sobre rotas HTTP ou frameworks web (FastAPI).
- **Não** faz consultas SQL diretas. Ela solicita dados para a camada de `repositories`.
- Recebe dados de entrada validados, processa a lógica de negócio e repassa para salvar/recuperar.

## Arquivos e Módulos
- **`auth_service.py`**: Intermedia o processo de registro de usuário e a validação de senhas para a geração e liberação de acesso via token JWT.
- **`desafio_service.py`**: Orquestra a regra de negócio para criar desafios e o fluxo do processamento de submissões dos alunos.
- **`enquete_service.py`**: Contém a lógica de negócio para certificar que os votos e o registro de enquetes são processados dentro do limite permitido pela turma.
- **`formacao_service.py`**: Invoca o algoritmo da camada `core` (Zig-Zag) e formata a resposta após salvar os alunos recém balanceados nas equipes.
- **`gamificacao_service.py`**: É o motor do sistema de conquistas; define e orquestra a lógica de recompensas, distribuição de XP (experiência), progressão de nível e bloqueio/desbloqueio de medalhas.
- **`mini_prova_service.py`**: Módulo vital, fortemente focado na regra estrita de negócio das Mini-Provas sob pressão. Coordena cronômetros (calculando diffs de timestamp), autoriza a entrada na tentativa, executa o cálculo de notas automático com base nas alternativas corretas.
- **`missao_service.py`**: Gerencia o fluxo complexo de missões, destravando as recompensas caso o aluno atinja um alvo estabelecido pela trilha do professor.
