# Camada Providers (Estratégias de Persistência)

## Responsabilidade
Implementa o **Provider Pattern**. Contém as implementações concretas de acesso ao banco de dados e outras tecnologias externas (ex: conexões SQL cruas, integrações com APIs terceiras).

## Regras
- Deve implementar uma interface comum (ex: `DatabaseProvider`) para que a estratégia de banco de dados possa ser trocada sem alterar o restante do sistema.
- Se comunica diretamente com a camada de `database/` para obter sessões de conexão ativa.
