# Camada Pages (Streamlit UI)

## Responsabilidade
Responsável pela interface do usuário construída com a biblioteca **Streamlit**. É a camada que renderiza telas, formulários, botões, tabelas e gráficos.

## Regras
- **Não** deve conter regras de negócio complexas.
- **Não** deve acessar o banco de dados diretamente.
- Deve se comunicar com o backend FastAPI através de requisições HTTP (usando `requests` do Python ou similar) enviando e recebendo dados no formato JSON.
