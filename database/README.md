# Camada Database (Conectores)

## Responsabilidade
Guarda os arquivos de configuração de banco de dados, inicialização de pool de conexões (Supabase/PostgreSQL) e scripts de setup de tabelas (Migrations/DDL).

## Regras
- Deve carregar segredos e dados de conexão diretamente do arquivo `.env`.
- Fornece funções geradoras de conexão (`get_db`) que são utilizadas pelos Providers.

## Arquivos e Módulos
- **`schema.sql`**: Contém o DDL (Data Definition Language) de todo o banco de dados. Este arquivo declara a estrutura física das tabelas de Alunos, Professores, Desafios, Provas, Missões e Gamificação, bem como funções e triggers SQL para RPCs (Remote Procedure Calls).
- **`__init__.py`**: Script de exportação que possivelmente instanciará a engine e session makers do SQLAlchemy ou drivers correspondentes.
