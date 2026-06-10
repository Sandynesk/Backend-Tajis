# Camada Repositories (Acesso aos Dados)

## Responsabilidade
Funciona como um intermediário entre a camada de regras de negócio (`services/`) e a infraestrutura de banco de dados (`providers/`). Ela define como os dados são obtidos e salvos.

## Regras
- Interage diretamente com a camada de `providers` (que por sua vez interage com o banco de dados Supabase/SQL).
- Centraliza operações de CRUD (Create, Read, Update, Delete) de entidades específicas (ex: `AlunoRepository`).
- Permite que a camada de serviços obtenha entidades limpas sem precisar saber como o SQL ou o banco de dados está estruturado.
