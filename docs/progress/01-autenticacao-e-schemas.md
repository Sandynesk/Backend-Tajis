# Progresso: Autenticação, Schemas e Integração Inicial (Sprint 1)

## O que foi desenvolvido

Nesta iteração inicial do desenvolvimento do backend, o foco foi estruturar as bases fundamentais de segurança, modelagem de dados e a integração arquitetural da aplicação utilizando o FastAPI e o banco de dados Supabase via Provider Pattern.

### 1. Provider Pattern & Supabase
- **`database/schema.sql`**: Criado o schema DDL relacional completo de acordo com o planejamento do projeto (entidades globais, desafios, mini-provas, gamificação, equipes e missões). O arquivo permite aplicar as tabelas no Supabase via Painel Web ou via CLI (migrations).
- **`database/__init__.py`**: Configurado o cliente de conexão oficial do Supabase.
- **`providers/`**: Estabelecido o Provider Pattern.
  - Criada a interface `DatabaseProvider` que abstrai as operações de banco.
  - Implementado o `SupabaseProvider`, que traduz operações CRUD genéricas (`fetch_all`, `insert`, etc.) para a API REST do Supabase.
  - Criada a `ProviderFactory` para injeção de dependência e facilidade na troca de tecnologias no futuro.

### 2. Autenticação e Segurança (Core)
- **Ajuste de Dependências**: Substituímos o pacote de JWT padrão para o `python-jose[cryptography]`, garantindo o padrão oficial do FastAPI. Incluímos o `email-validator` para suporte completo ao tipo `EmailStr`.
- **`core/config.py`**: Utilização do `pydantic-settings` para carregamento unificado de variáveis de ambiente (`SECRET_KEY`, acessos do Supabase).
- **`core/security.py`**: Configuração do `passlib` (bcrypt) para hashing bidirecional de senhas e geração/codificação segura de Tokens JWT.

### 3. Modelagem de Dados (Schemas)
Foram definidos os modelos de entrada (Create) e de saída (Response) na pasta `models/` baseados no Pydantic:
- **`models/user.py`**: Contém validações estritas (ex: tamanho de senha) para `Aluno` e `Professor`, além dos modelos de payload de Login e Token.
- **`models/disciplina.py` e `models/turma.py`**: Schemas para lidar com o ciclo acadêmico.

### 4. Acesso a Dados e Negócios
- **Repositories**: Criados `aluno_repository.py` e `professor_repository.py` utilizando o `DatabaseProvider`. Isso isola completamente os serviços da tecnologia subjacente (Supabase).
- **Services**: Criado `auth_service.py` para orquestrar as regras de negócio: validação se email já existe, processo de hashing de senhas antes da inserção e coordenação do fluxo de login, diferenciando alunos e professores dinamicamente.

### 5. Exposição e Autorização (API)
- **`dependencies/auth.py`**: Implementada a injeção de dependência via cabeçalho `Bearer` do OAuth2. O fluxo decodifica o JWT, identifica a procedência da role (`aluno` ou `professor`) e já busca os dados sanitizados do banco.
- **`api/auth.py`**: Três rotas principais exportadas:
  - `POST /auth/register/aluno`
  - `POST /auth/register/professor`
  - `POST /auth/login`
- O `main.py` foi atualizado para acoplar esse roteador, permitindo os testes diretos via Swagger UI.

## Próximos Passos Sugeridos
- Iniciar a implementação dos módulos de **Turma e Disciplina** (Endpoints, Services e Repositories).
- Expandir a infraestrutura para o sistema de **Desafios** e **Mini-Provas**, já com rotas protegidas (exigindo que as ações de criação sejam feitas apenas por `Professor`).
