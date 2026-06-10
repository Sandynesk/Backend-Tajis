# Camada Database (Conectores)

## Responsabilidade
Guarda os arquivos de configuração de banco de dados, inicialização de pool de conexões (Supabase/PostgreSQL) e scripts de setup de tabelas (Migrations/DDL).

## Regras
- Deve carregar segredos e dados de conexão diretamente do arquivo `.env`.
- Fornece funções geradoras de conexão (`get_db`) que são utilizadas pelos Providers.
