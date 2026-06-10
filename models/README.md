# Camada Models (Entidades e Schemas)

## Responsabilidade
Centraliza a definição de todas as estruturas de dados do sistema:
1. **Entidades do Banco (Models):** Representam as tabelas e colunas físicas do banco de dados relacional.
2. **Schemas Pydantic (Validação):** Estruturas de dados para validação de requisições de entrada (Request Payloads) e respostas de saída (Response Schemas) da API.

## Regras
- Devem ser puramente declarativos (sem regras de negócio).
- Servem como contrato de tipo entre o banco de dados, o backend e a API.
