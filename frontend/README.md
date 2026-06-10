# Interface Gráfica (Frontend)

Esta pasta contém o cliente web do projeto **TAJI**, construído utilizando o framework [Streamlit](https://streamlit.io/). O objetivo desta aplicação é consumir a API REST (FastAPI) do backend e oferecer uma interface interativa e gamificada para Professores e Alunos.

## Estrutura de Arquivos Adicionados

- `app.py`: O ponto de entrada principal do Streamlit. Controla o redirecionamento de usuários logados (para o Dashboard) e não logados (para o Login).
- `api_client.py`: Módulo centralizado responsável por todas as requisições HTTP (`requests`) para o backend FastAPI. Ele injeta os tokens JWT armazenados na sessão de forma automática e intercepta erros de sessão expirada (`401`).
- `utils.py`: Funções auxiliares vitais, incluindo `check_login()` para a proteção das rotas e `logout()` para gestão do estado e segurança da aplicação.
- `requirements.txt`: Dependências do Python exclusivas para o funcionamento do Streamlit.
- `pages/`: Diretório que contém todas as abas e páginas navegáveis (o Streamlit reconhece essas páginas nativamente na barra lateral):
  - `01_🔐_Login.py`: Interface de autenticação e registro.
  - `02_🏠_Dashboard.py`: Tela principal pós-login, adaptativa de acordo com o cargo (Aluno/Professor).
  - `03_📚_Desafios.py`: Lista e controle de desafios das disciplinas.
  - `04_📝_Mini_Provas.py`: Sistema de provas dinâmico, que inclui um inovador timer com `html/javascript` injetado para não causar interrupções de estado na re-renderização do Python.
  - `05_🏆_Gamificacao.py`: Ranking e acompanhamento de XP e Medalhas.
  - `06_🎯_Missoes.py`: Acompanhamento de jornadas educativas e suas etapas.
  - `07_👥_Formacao_Equipes.py`: Geração e acompanhamento dos agrupamentos inteligentes da turma.
  - `08_📊_Enquetes.py`: Feedback instantâneo renderizando gráficos de barras dos votos dos alunos.

## Como Iniciar

1. Certifique-se de que o backend FastAPI esteja rodando (em geral na porta 8000).
2. Instale as dependências: `pip install -r requirements.txt`.
3. Inicie a interface visual: `streamlit run app.py`.
