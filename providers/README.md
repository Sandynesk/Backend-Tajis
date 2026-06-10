# Camada Providers (Estratégias de Persistência)

## Responsabilidade
Implementa o **Provider Pattern**. Contém as implementações concretas de acesso ao banco de dados e outras tecnologias externas (ex: conexões SQL cruas, integrações com APIs terceiras).

## Regras
- Deve implementar uma interface comum (ex: `DatabaseProvider`) para que a estratégia de banco de dados possa ser trocada sem alterar o restante do sistema.
- Se comunica diretamente com a camada de `database/` para obter sessões de conexão ativa.

## Arquivos e Módulos
- **`database_provider.py`**: Define a interface base e comum para qualquer provedor de banco de dados. Declara os métodos de execução (fetch, insert, rpc, transaction) que devem ser sobrescritos pelas implementações concretas.
- **`supabase_provider.py`**: A implementação concreta do `database_provider` utilizando o cliente Python do Supabase (ou `postgrest`), garantindo a comunicação direta com a infraestrutura em nuvem configurada.
- **`factory.py`**: Módulo responsável pelo Padrão Factory, permitindo a injeção e seleção do provedor (no caso, instanciando e servindo o SupabaseProvider ativamente para os repositórios).
