# Camada Services (Regras de Negócio)

## Responsabilidade
É o coração do backend. Contém toda a lógica de negócio do sistema (cálculo de médias, validação de regras de tempo para mini-provas, processamento de gamificação e pontos, algoritmo de distribuição de equipes).

## Regras
- **Não** sabe nada sobre rotas HTTP ou frameworks web (FastAPI).
- **Não** faz consultas SQL diretas. Ela solicita dados para a camada de `repositories`.
- Recebe dados de entrada validados, processa a lógica de negócio e repassa para salvar/recuperar.
