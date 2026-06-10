-- =========================================================================
-- ESQUEMA DE BANCO DE DADOS (DDL) - PROJETO INTEGRADOR BACKEND (TAJI)
-- =========================================================================

-- Habilitar a extensão UUID se não estiver ativa
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -------------------------------------------------------------------------
-- 1. ENTIDADES GLOBAIS
-- -------------------------------------------------------------------------

-- Tabela: Professor
CREATE TABLE IF NOT EXISTS professor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    departamento VARCHAR(255),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Aluno
CREATE TABLE IF NOT EXISTS aluno (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nivel_atual INT DEFAULT 1 NOT NULL,
    xp_acumulado INT DEFAULT 0 NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Disciplina
CREATE TABLE IF NOT EXISTS disciplina (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Turma
CREATE TABLE IF NOT EXISTS turma (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    disciplina_id UUID REFERENCES disciplina(id) ON DELETE CASCADE NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE SET NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela de Relação: Turma <-> Aluno (Muitos para Muitos)
CREATE TABLE IF NOT EXISTS turma_aluno (
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE,
    PRIMARY KEY (turma_id, aluno_id)
);

-- -------------------------------------------------------------------------
-- 2. CONTEXTO: SISTEMA DE DESAFIOS
-- -------------------------------------------------------------------------

-- Tabela: Desafio
CREATE TABLE IF NOT EXISTS desafio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    prazo TIMESTAMP WITH TIME ZONE NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Submissao
CREATE TABLE IF NOT EXISTS submissao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    desafio_id UUID REFERENCES desafio(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    conteudo_resposta TEXT NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Voto
CREATE TABLE IF NOT EXISTS voto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submissao_id UUID REFERENCES submissao(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    voto INT CHECK (voto IN (-1, 1)) NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (submissao_id, aluno_id) -- Garante um voto por aluno por submissão
);

-- Tabela: Nota
CREATE TABLE IF NOT EXISTS nota (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submissao_id UUID REFERENCES submissao(id) ON DELETE CASCADE UNIQUE NOT NULL,
    valor NUMERIC(4, 2) CHECK (valor >= 0 AND valor <= 10.00) NOT NULL,
    avaliado_por UUID REFERENCES professor(id) ON DELETE SET NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- -------------------------------------------------------------------------
-- 3. CONTEXTO: MINI-PROVAS
-- -------------------------------------------------------------------------

-- Tabela: Prova
CREATE TABLE IF NOT EXISTS prova (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    duracao_segundos INT DEFAULT 300 NOT NULL, -- Padrão 5 minutos (300 segundos)
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Questao
CREATE TABLE IF NOT EXISTS questao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prova_id UUID REFERENCES prova(id) ON DELETE CASCADE NOT NULL,
    enunciado TEXT NOT NULL,
    alternativa_a TEXT NOT NULL,
    alternativa_b TEXT NOT NULL,
    alternativa_c TEXT NOT NULL,
    alternativa_d TEXT NOT NULL,
    alternativa_correta CHAR(1) CHECK (alternativa_correta IN ('A', 'B', 'C', 'D')) NOT NULL,
    pontos INT DEFAULT 10 NOT NULL
);

-- Tabela: Tentativa (Controle de tempo da prova)
CREATE TABLE IF NOT EXISTS tentativa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prova_id UUID REFERENCES prova(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    iniciado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    finalizado_em TIMESTAMP WITH TIME ZONE,
    UNIQUE (prova_id, aluno_id) -- Apenas uma tentativa por prova por aluno
);

-- Tabela: Resposta da Questão
CREATE TABLE IF NOT EXISTS resposta_questao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tentativa_id UUID REFERENCES tentativa(id) ON DELETE CASCADE NOT NULL,
    questao_id UUID REFERENCES questao(id) ON DELETE CASCADE NOT NULL,
    alternativa_assinalada CHAR(1) CHECK (alternativa_assinalada IN ('A', 'B', 'C', 'D')) NOT NULL,
    UNIQUE (tentativa_id, questao_id)
);

-- -------------------------------------------------------------------------
-- 4. CONTEXTO: GAMIFICAÇÃO
-- -------------------------------------------------------------------------

-- Tabela: Medalha (Catálogo)
CREATE TABLE IF NOT EXISTS medalha (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    icone_url VARCHAR(512),
    xp_recompensa INT DEFAULT 50 NOT NULL
);

-- Tabela: Conquista (Ligação Aluno <-> Medalha)
CREATE TABLE IF NOT EXISTS conquista (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    medalha_id UUID REFERENCES medalha(id) ON DELETE CASCADE NOT NULL,
    conquistada_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (aluno_id, medalha_id)
);

-- Tabela: Tabela de Níveis (Experiência necessária por nível)
CREATE TABLE IF NOT EXISTS nivel (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_nivel INT UNIQUE NOT NULL,
    xp_necessario INT NOT NULL
);

-- Tabela: Log de Histórico de Pontos (Transacional)
CREATE TABLE IF NOT EXISTS historico_pontos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    pontos INT NOT NULL, -- Pode ser positivo (ganho) ou negativo (perda)
    motivo VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- -------------------------------------------------------------------------
-- 5. CONTEXTO: FEEDBACK INSTANTÂNEO
-- -------------------------------------------------------------------------

-- Tabela: Enquete
CREATE TABLE IF NOT EXISTS enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    ativa BOOLEAN DEFAULT TRUE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Pergunta da Enquete
CREATE TABLE IF NOT EXISTS pergunta (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    enquete_id UUID REFERENCES enquete(id) ON DELETE CASCADE NOT NULL,
    texto_pergunta TEXT NOT NULL
);

-- Tabela: Resposta da Enquete
CREATE TABLE IF NOT EXISTS resposta_enquete (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pergunta_id UUID REFERENCES pergunta(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    valor_resposta TEXT NOT NULL, -- Pode ser nota de 1 a 5 ou sim/não
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (pergunta_id, aluno_id)
);

-- -------------------------------------------------------------------------
-- 6. CONTEXTO: FORMAÇÃO DE EQUIPES
-- -------------------------------------------------------------------------

-- Tabela: Equipe
CREATE TABLE IF NOT EXISTS equipe (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela de Relação: Integrante Equipe
CREATE TABLE IF NOT EXISTS integrante_equipe (
    equipe_id UUID REFERENCES equipe(id) ON DELETE CASCADE,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE,
    PRIMARY KEY (equipe_id, aluno_id)
);

-- Tabela: Habilidade
CREATE TABLE IF NOT EXISTS habilidade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela de Relação: Aluno <-> Habilidade
CREATE TABLE IF NOT EXISTS aluno_habilidade (
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE,
    habilidade_id UUID REFERENCES habilidade(id) ON DELETE CASCADE,
    nivel_proficiencia INT CHECK (nivel_proficiencia >= 1 AND nivel_proficiencia <= 5) DEFAULT 3 NOT NULL,
    PRIMARY KEY (aluno_id, habilidade_id)
);

-- Tabela: Critério de Formação
CREATE TABLE IF NOT EXISTS criterio_equipe (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL,
    tipo_criterio VARCHAR(100) NOT NULL, -- Ex: 'balanceado_por_habilidade', 'aleatorio'
    configuracao JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- -------------------------------------------------------------------------
-- 7. CONTEXTO: MISSÕES EDUCACIONAIS
-- -------------------------------------------------------------------------

-- Tabela: Missão
CREATE TABLE IF NOT EXISTS missao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Tabela: Etapa da Missão
CREATE TABLE IF NOT EXISTS etapa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    missao_id UUID REFERENCES missao(id) ON DELETE CASCADE NOT NULL,
    ordem INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    xp_recompensa INT DEFAULT 100 NOT NULL
);

-- Tabela: Progresso da Missão
CREATE TABLE IF NOT EXISTS progresso_missao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    etapa_id UUID REFERENCES etapa(id) ON DELETE CASCADE NOT NULL,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (aluno_id, etapa_id)
);

-- Tabela: Recompensa Adicional
CREATE TABLE IF NOT EXISTS recompensa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    missao_id UUID REFERENCES missao(id) ON DELETE CASCADE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL, -- Ex: 'xp', 'medalha', 'custom'
    valor_xp INT DEFAULT 0,
    medalha_id UUID REFERENCES medalha(id) ON DELETE SET NULL
);
