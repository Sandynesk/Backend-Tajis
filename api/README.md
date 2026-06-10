# Camada API (FastAPI)

## Responsabilidade
Contém os roteadores, endpoints e controladores da API HTTP construída com o **FastAPI**. Define a porta de entrada da API que o Streamlit ou qualquer outro cliente irá consumir.

## Regras
- Recebe as requisições HTTP, valida os parâmetros de entrada (Payloads, Query Params) usando os Schemas do Pydantic.
- **Não** implementa lógica de negócio. Ela apenas chama a camada `services` correspondente e retorna os resultados formatados (HTTP 200, 201, 400, etc.).
- Aplica middlewares de segurança, como validação de tokens JWT (autenticação) e controle de permissões.

## Arquivos e Módulos
- `auth.py`: Endpoints de autenticação, login e registro de usuários (Alunos e Professores).
- `desafios.py`: Endpoints para criação, listagem e submissão de respostas a desafios.
- `enquetes.py`: Endpoints de criação de enquetes e recebimento de votos.
- `formacao.py`: Endpoints para execução do algoritmo de formação inteligente de equipes.
- `gamificacao.py`: Endpoints que fornecem o ranking global, progresso de nível e galeria de medalhas.
- `mini_provas.py`: Endpoints para criação de avaliações temporizadas, além de iniciar e responder tentativas.
- `missoes.py`: Endpoints para controle de missões educacionais (trilhas de aprendizagem).
