# Arquitetura e Stack Tecnológica

## Stack Sugerida
- **Linguagem Principal:** Python
- **Framework API:** FastAPI (APIs REST)
- **Banco de Dados:** Supabase / PostgreSQL (SQL Relacional)
- **Frontend:** Streamlit
- **Versionamento:** Git e GitHub

## Arquitetura Geral do Sistema
O sistema adota uma arquitetura em camadas focada em desacoplamento, utilizando o **Provider Pattern**.

A aplicação será dividida pelos grupos da sala, onde cada grupo (`grupo1`, `grupo2`, etc.) possuirá sua própria branch no GitHub e seu próprio banco no Supabase. 

## Provider Pattern
O *Provider Pattern* tem como objetivo separar a regra de negócio da estratégia de acesso a dados.
- **Interface Base (`DatabaseProvider`):** Define os contratos (ex: `get_all`, `create`).
- **Provider Factory:** A fábrica para instanciar as conexões. Exemplo: `provider = ProviderFactory.create("sql")`
Isso permite trocar o banco de dados no futuro sem alterar as camadas superiores.

## Estrutura de Diretórios Obrigatória
O projeto *deve* obedecer a seguinte estrutura de arquivos:
```text
project/
│
├── pages/          # Telas do Streamlit e interface.
├── services/       # Regras de negócio e processamento.
├── repositories/   # Acesso aos dados utilizando os Providers.
├── providers/      # Implementação do Provider Pattern (Estratégias de persistência).
├── api/            # Implementação dos endpoints com FastAPI.
├── models/         # Entidades do sistema (Modelos e Schemas Pydantic).
├── database/       # Configuração de conexão ao banco.
├── docs/           # Documentação técnica do projeto (você está aqui).
└── utils/          # Funções utilitárias e ajudantes gerais.
```
