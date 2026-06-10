# Camada Core (Configurações e Segurança)

## Responsabilidade
A pasta `core/` concentra as configurações fundamentais, variáveis de ambiente, lógica criptográfica e instâncias fundamentais da infraestrutura de algoritmos da aplicação.

## Arquivos e Módulos
- **`config.py`**: Utiliza o `pydantic-settings` para carregar de forma segura as variáveis de ambiente a partir do arquivo `.env` (ex: `SECRET_KEY`, `ALGORITHM`, credenciais do Supabase). Garante tipagem e validação da configuração central.
- **`security.py`**: Agrupa a lógica criptográfica da aplicação, fazendo o hashing de senhas com `bcrypt` e gerenciando a criação/assinatura de tokens JWT.
- **`algoritmos.py`**: Centraliza os algoritmos de balanceamento e distribuição, como o algoritmo Zig-Zag utilizado na divisão automatizada e justa de alunos para as formações de equipe.
- **`constants.py`**: Define valores constantes globais, como limites de níveis de gamificação e patamares de experiência (XP).
- **`init_db.py`**: Script essencial ou definições para pré-popular (seed) e inicializar a conexão com a infraestrutura do banco de dados (Supabase/PostgreSQL).
