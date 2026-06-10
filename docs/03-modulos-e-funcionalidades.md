# Módulos e Funcionalidades

A plataforma é dividida em 6 módulos principais, focados em metodologias ativas:

## 1. Sistema de Desafios
**Objetivo:** Permitir que professores criem desafios relacionados a disciplinas e assuntos específicos.
- **Professor:** Cadastra desafios, edita, define disciplinas e prazos, visualiza o ranking.
- **Aluno:** Visualiza desafios, envia respostas (submissões) e acompanha sua pontuação.
- **Lógica Central:** Cálculo automático da média final, sistema de votação, geração do ranking geral e histórico.

## 2. Mini-Provas (Avaliações sob pressão)
**Objetivo:** Criar um sistema de avaliações rápidas e gamificadas.
- **Professor:** Cadastra provas e questões, acompanha estatísticas e desempenho da turma.
- **Aluno:** Responde sob tempo cronometrado e visualiza a própria pontuação.
- **Regras Estritas de Tempo:**
  - 5 minutos de tempo total máximo.
  - 5 questões (média de 1 minuto por questão).
  - Cronômetro global (da prova) e por questão.
  - Correção estritamente automática pelo backend.

## 3. Sistema de Gamificação
**Objetivo:** Criar mecanismos de engajamento contínuo através de pontuações e progressão.
- **Lógica Central:**
  - O sistema deve calcular pontos concedidos por atividades executadas (fazer prova, completar desafio).
  - Controle de 'Streaks' (dias consecutivos).
  - Progressão de Nível do usuário.
  - Ranking semanal e geral da plataforma.
  - Atribuição de Medalhas e recompensas por conquistas.

## 4. Feedback Instantâneo
**Objetivo:** Interação rápida entre professor e turma durante aulas ou pós-aulas.
- **Funcionalidades:** Criação de enquetes rápidas, recebimento de respostas dos alunos em tempo real, compilação de estatísticas e renderização de gráficos.

## 5. Formação de Equipes
**Objetivo:** Formar grupos automaticamente baseados em lógicas estruturadas e não apenas aleatoriedade.
- **Funcionalidades:** Geração de equipes automáticas pelo backend, visando balancear o desempenho ou o mapa de habilidades dos integrantes. O professor pode definir os critérios de agrupamento e permitir ou não a reorganização.

## 6. Missões Educacionais
**Objetivo:** Criar jornadas de aprendizagem cadenciadas baseadas em trilhas/etapas.
- **Funcionalidades:** Criação de missões divididas em etapas, sistema de progressão contínua onde a próxima etapa é desbloqueada de acordo com as ações do usuário (Desbloqueios), gerando recompensas finais e pontuação atrelada ao motor de Gamificação.
