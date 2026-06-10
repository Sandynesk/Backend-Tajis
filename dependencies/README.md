# Camada Dependencies (Injeção e Autorização)

## Responsabilidade
A pasta `dependencies/` armazena as dependências injetáveis (`Depends`) utilizadas pelos roteadores do FastAPI. O objetivo principal é manter o código das rotas (API) extremamente limpo, extraindo validações e resoluções comuns para cá.

## O que contém?
- **`auth.py`**: Gerencia a lógica de extração, decodificação e validação de tokens JWT. 
  - `get_current_user`: Lê o token do cabeçalho de autorização, decodifica, identifica o papel (role) do usuário e busca seus dados completos no banco (via repositórios e `DatabaseProvider`).
  - `get_current_aluno` e `get_current_professor`: Extensões da dependência anterior que impõem controle de acesso (RBAC), rejeitando a requisição (HTTP 403 Forbidden) caso o usuário não tenha o nível de privilégio exigido.
