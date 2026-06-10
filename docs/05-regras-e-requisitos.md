# Regras, Requisitos e Restrições do Sistema

## Requisitos Não Funcionais
1. **Segurança e Acesso:** O sistema precisa garantir o controle de acesso de forma estrita (Login), segmentando o que um Aluno e o que um Professor pode fazer (Autorização).
2. **Validação de Dados:** O backend (via FastAPI / Pydantic) deve validar todos os dados recebidos antes de persistir no banco.
3. **Auditoria (Logs):** Registro sistemático de operações importantes para auditoria e acompanhamento.
4. **Tratamento de Erros:** Respostas controladas, padronizadas e seguras (não vazando stack trace do servidor em produção).
5. **Escalabilidade:** A aplicação deve ser construída pensando em escalar futuramente, por isso a exigência da separação em camadas (`services/`, `repositories/`, `providers/`).

## Regras de Negócio Globais
- **Provas com Tempo Limite (Backend-Driven):** O controle de tempo das mini-provas *não* deve confiar apenas no Frontend. O Backend deve registrar o início da "Tentativa" e recusar submissões após os 5 minutos previstos de forma irrevogável.
- **Correção Automática:** Todas as questões das mini-provas precisam suportar verificação de acerto/erro automática (sem intervenção do professor).
- **Engine Gamificada Reativa:** O cálculo de progressão de nível e a entrega de pontos não deve ser uma chamada manual do usuário, mas um reflexo passivo/automático (evento) sempre que concluir uma missão, prova ou desafio.
- **Isolamento de Persistência:** É absolutamente probido que as rotas da `api/` (os Endpoints) realizem consultas SQL ou instanciem o driver do Supabase diretamente. Tudo deve passar por `services/` -> `repositories/` -> `providers/`.

## Restrições do Projeto Integrador
- Os grupos não compartilham banco de dados. Cada sub-grupo terá um Supabase distinto.
- Cada grupo deverá manter suas atualizações na sua própria branch no GitHub.
- É obrigatório o uso das camadas e pastas especificadas na visão de arquitetura.
