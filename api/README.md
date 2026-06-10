# Camada API (FastAPI)

## Responsabilidade
Contém os roteadores, endpoints e controladores da API HTTP construída com o **FastAPI**. Define a porta de entrada da API que o Streamlit ou qualquer outro cliente irá consumir.

## Regras
- Recebe as requisições HTTP, valida os parâmetros de entrada (Payloads, Query Params) usando os Schemas do Pydantic.
- **Não** implementa lógica de negócio. Ela apenas chama a camada `services` correspondente e retorna os resultados formatados (HTTP 200, 201, 400, etc.).
- Aplica middlewares de segurança, como validação de tokens JWT (autenticação) e controle de permissões.
