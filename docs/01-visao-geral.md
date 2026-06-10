# Visão Geral do Projeto Integrador Backend

## Título e Descrição Geral
O projeto consiste no desenvolvimento de uma plataforma educacional baseada em metodologias ativas utilizando uma arquitetura backend moderna. Seu objetivo é engajar os alunos através de dinâmicas interativas e gamificadas.

## Visão e Objetivo Principal
A visão do projeto é aproximar os alunos de um ambiente real de desenvolvimento profissional. 
O problema que ele resolve é a falta de engajamento no modelo tradicional de ensino, utilizando ferramentas modernas (Gamificação, Feedback em tempo real, Mini-Provas sob pressão) para tornar o aprendizado mais dinâmico.

## Público-Alvo e Personas
1. **Professor:** Responsável por criar os desafios, cadastrar mini-provas, criar missões, iniciar enquetes para feedback instantâneo e gerenciar os critérios para formação de equipes.
2. **Aluno:** O usuário final que irá acessar a plataforma para realizar os desafios, responder às mini-provas contra o tempo, ganhar recompensas/medalhas, subir de nível na gamificação e visualizar seu ranking.

## Fluxo Básico da Aplicação
A aplicação possui um fluxo de comunicação bem estabelecido:
`Frontend (Streamlit) -> HTTP/JSON -> Backend API (FastAPI) -> Services (Regras) -> Providers -> Repositories -> Supabase (PostgreSQL)`
