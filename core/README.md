# Camada Core (Configurações e Segurança)

## Responsabilidade
A pasta `core/` concentra as configurações fundamentais, variáveis de ambiente e as políticas de segurança essenciais da aplicação.

## O que contém?
- **`config.py`**: Utiliza o `pydantic-settings` para carregar de forma segura as variáveis de ambiente a partir do arquivo `.env` (ex: `SECRET_KEY`, `ALGORITHM`, credenciais do Supabase). Isso garante que toda a aplicação consuma as mesmas configurações centralizadas, com tipagem e validação.
- **`security.py`**: Agrupa a lógica criptográfica da aplicação. Contém as funções para:
  - Fazer o hashing de senhas utilizando `passlib` com o algoritmo `bcrypt`.
  - Verificar a validade de senhas.
  - Criar e assinar tokens JWT utilizando a biblioteca `python-jose[cryptography]`.
