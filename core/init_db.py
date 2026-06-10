import os
import logging
from providers import ProviderFactory
from supabase import Client

logger = logging.getLogger(__name__)

# Script SQL para criação das tabelas usando IF NOT EXISTS.
# As chaves primárias e estrangeiras de usuários/turmas usam UUID para compatibilidade
# com o schema já existente (ex: models/user.py e database/schema.sql).
# Tabelas base (aluno, professor, turma) são garantidas aqui para tornar o script autossuficiente.
SCHEMA_SQL = """
-- Extensão necessária para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabelas Base (se não existirem)
CREATE TABLE IF NOT EXISTS professor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    departamento VARCHAR(255),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS aluno (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nivel_atual INT DEFAULT 1 NOT NULL,
    xp_acumulado INT DEFAULT 0 NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplina (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS turma (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    disciplina_id UUID REFERENCES disciplina(id) ON DELETE CASCADE NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE SET NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- MÓDULO DE DESAFIOS
CREATE TABLE IF NOT EXISTS desafios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    pontos INT NOT NULL CHECK (pontos > 0),
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS desafios_alunos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    desafio_id UUID REFERENCES desafios(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    status VARCHAR(50) DEFAULT 'pendente' NOT NULL,
    data_conclusao TIMESTAMP WITH TIME ZONE,
    nota FLOAT,
    UNIQUE(desafio_id, aluno_id)
);

-- MÓDULO DE MINI-PROVAS
CREATE TABLE IF NOT EXISTS mini_provas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    tempo_limite_segundos INT NOT NULL DEFAULT 300,
    nota_minima_aprovacao FLOAT DEFAULT 0.7 NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS questoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mini_prova_id UUID REFERENCES mini_provas(id) ON DELETE CASCADE NOT NULL,
    enunciado TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('multipla_escolha', 'verdadeiro_falso', 'dissertativa')),
    alternativas JSONB,
    pontuacao FLOAT NOT NULL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS tentativas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mini_prova_id UUID REFERENCES mini_provas(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    data_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    data_fim TIMESTAMP WITH TIME ZONE,
    nota_final FLOAT,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    UNIQUE(mini_prova_id, aluno_id, concluida) -- Permite apenas uma tentativa por prova ou requer lógica no backend
);

CREATE TABLE IF NOT EXISTS respostas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tentativa_id UUID REFERENCES tentativas(id) ON DELETE CASCADE NOT NULL,
    questao_id UUID REFERENCES questoes(id) ON DELETE CASCADE NOT NULL,
    alternativa_escolhida CHAR(1),
    texto_resposta TEXT,
    UNIQUE(tentativa_id, questao_id)
);

-- MÓDULO DE GAMIFICAÇÃO
CREATE TABLE IF NOT EXISTS acoes_gamificacao (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) UNIQUE NOT NULL,
    pontos INT NOT NULL CHECK (pontos >= 0)
);

CREATE TABLE IF NOT EXISTS pontuacoes (
    id SERIAL PRIMARY KEY,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    acao_id INT REFERENCES acoes_gamificacao(id) ON DELETE CASCADE NOT NULL,
    pontos_ganhos INT NOT NULL,
    data TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    descricao TEXT
);

CREATE INDEX IF NOT EXISTS idx_pontuacoes_aluno_id ON pontuacoes(aluno_id);
CREATE INDEX IF NOT EXISTS idx_pontuacoes_data ON pontuacoes(data);

CREATE TABLE IF NOT EXISTS niveis (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    pontos_minimos INT NOT NULL,
    icon VARCHAR(512)
);

CREATE INDEX IF NOT EXISTS idx_niveis_pontos_minimos ON niveis(pontos_minimos);

CREATE TABLE IF NOT EXISTS medalhas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    criterio TEXT NOT NULL,
    icon VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS medalhas_alunos (
    id SERIAL PRIMARY KEY,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    medalha_id INT REFERENCES medalhas(id) ON DELETE CASCADE NOT NULL,
    data_concedida TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(aluno_id, medalha_id)
);

-- MÓDULO DE MISSÕES
CREATE TABLE IF NOT EXISTS missoes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE,
    ativa BOOLEAN DEFAULT TRUE NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('individual', 'turma')),
    pontos_recompensa INT NOT NULL DEFAULT 0,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    data_fim TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS etapas_missao (
    id SERIAL PRIMARY KEY,
    missao_id INT REFERENCES missoes(id) ON DELETE CASCADE NOT NULL,
    ordem INT NOT NULL CHECK (ordem > 0),
    descricao TEXT NOT NULL,
    tipo_acao VARCHAR(255) NOT NULL,
    meta INT NOT NULL CHECK (meta > 0),
    pontos_etapa INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS progresso_missao (
    id SERIAL PRIMARY KEY,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    missao_id INT REFERENCES missoes(id) ON DELETE CASCADE NOT NULL,
    etapa_atual INT NOT NULL DEFAULT 1,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    data_inicio TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    data_conclusao TIMESTAMP WITH TIME ZONE,
    UNIQUE(aluno_id, missao_id)
);

CREATE TABLE IF NOT EXISTS progresso_etapa (
    id SERIAL PRIMARY KEY,
    progresso_id INT REFERENCES progresso_missao(id) ON DELETE CASCADE NOT NULL,
    etapa_id INT REFERENCES etapas_missao(id) ON DELETE CASCADE NOT NULL,
    contador INT NOT NULL DEFAULT 0,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    UNIQUE(progresso_id, etapa_id)
);

-- VIEWS DE RANKING
CREATE OR REPLACE VIEW ranking_geral_view AS
SELECT 
    a.id AS aluno_id,
    a.nome AS nome_aluno,
    COALESCE(SUM(p.pontos_ganhos), 0) AS pontos_total,
    COUNT(DISTINCT ma.medalha_id) AS medalhas
FROM aluno a
LEFT JOIN pontuacoes p ON a.id = p.aluno_id
LEFT JOIN medalhas_alunos ma ON a.id = ma.aluno_id
GROUP BY a.id, a.nome
ORDER BY pontos_total DESC;

-- A view semanal pode ser calculada dinamicamente, mas vamos criar uma RPC
-- para facilitar a chamada com limites e datas.
CREATE OR REPLACE FUNCTION get_ranking_semanal()
RETURNS TABLE (
    aluno_id UUID,
    nome_aluno VARCHAR,
    pontos_total BIGINT,
    medalhas BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id AS aluno_id,
        a.nome AS nome_aluno,
        COALESCE(SUM(p.pontos_ganhos), 0) AS pontos_total,
        COUNT(DISTINCT ma.medalha_id) AS medalhas
    FROM aluno a
    LEFT JOIN pontuacoes p ON a.id = p.aluno_id AND p.data >= (NOW() - INTERVAL '7 days')
    LEFT JOIN medalhas_alunos ma ON a.id = ma.aluno_id
    GROUP BY a.id, a.nome
    ORDER BY pontos_total DESC;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- FASE 5: FORMAÇÃO E ENQUETES
-- ==========================================

CREATE TABLE IF NOT EXISTS sessoes_formacao (
    id SERIAL PRIMARY KEY,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'concluida' NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS grupos (
    id SERIAL PRIMARY KEY,
    sessao_id INT REFERENCES sessoes_formacao(id) ON DELETE CASCADE NOT NULL,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS grupo_alunos (
    id SERIAL PRIMARY KEY,
    grupo_id INT REFERENCES grupos(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    UNIQUE(grupo_id, aluno_id)
);

CREATE TABLE IF NOT EXISTS enquetes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    turma_id UUID REFERENCES turma(id) ON DELETE CASCADE NOT NULL,
    professor_id UUID REFERENCES professor(id) ON DELETE CASCADE NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('unica', 'multipla')),
    ativa BOOLEAN DEFAULT TRUE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    data_fim TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS opcoes_enquete (
    id SERIAL PRIMARY KEY,
    enquete_id INT REFERENCES enquetes(id) ON DELETE CASCADE NOT NULL,
    texto VARCHAR(255) NOT NULL,
    contador INT DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS votos_enquete (
    id SERIAL PRIMARY KEY,
    enquete_id INT REFERENCES enquetes(id) ON DELETE CASCADE NOT NULL,
    aluno_id UUID REFERENCES aluno(id) ON DELETE CASCADE NOT NULL,
    UNIQUE(enquete_id, aluno_id)
);

-- RPC: Criar Sessão de Formação Atomicamente
CREATE OR REPLACE FUNCTION criar_sessao_formacao(sessao_data JSON, grupos_data JSON)
RETURNS JSON AS $$
DECLARE
    v_sessao_id INT;
    v_grupo_id INT;
    v_grupo JSON;
    v_aluno_id_str TEXT;
BEGIN
    INSERT INTO sessoes_formacao (turma_id, nome, status, professor_id)
    VALUES (
        (sessao_data->>'turma_id')::UUID,
        sessao_data->>'nome',
        'concluida',
        (sessao_data->>'professor_id')::UUID
    ) RETURNING id INTO v_sessao_id;

    FOR v_grupo IN SELECT * FROM json_array_elements(grupos_data)
    LOOP
        INSERT INTO grupos (sessao_id, nome)
        VALUES (v_sessao_id, v_grupo->>'nome')
        RETURNING id INTO v_grupo_id;

        FOR v_aluno_id_str IN SELECT * FROM json_array_elements_text(v_grupo->'alunos')
        LOOP
            INSERT INTO grupo_alunos (grupo_id, aluno_id)
            VALUES (v_grupo_id, v_aluno_id_str::UUID);
        END LOOP;
    END LOOP;

    RETURN json_build_object('sessao_id', v_sessao_id);
END;
$$ LANGUAGE plpgsql;

-- RPC: Registrar Voto Enquete Atomicamente
CREATE OR REPLACE FUNCTION registrar_voto_enquete(p_enquete_id INT, p_aluno_id UUID, p_opcoes_ids INT[])
RETURNS BOOLEAN AS $$
DECLARE
    v_ativa BOOLEAN;
    v_data_fim TIMESTAMP WITH TIME ZONE;
    v_opcao_id INT;
BEGIN
    SELECT ativa, data_fim INTO v_ativa, v_data_fim
    FROM enquetes WHERE id = p_enquete_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Enquete não encontrada';
    END IF;

    IF NOT v_ativa THEN
        RAISE EXCEPTION 'Enquete inativa';
    END IF;

    IF v_data_fim IS NOT NULL AND v_data_fim < timezone('utc'::text, now()) THEN
        RAISE EXCEPTION 'Prazo da enquete encerrado';
    END IF;

    INSERT INTO votos_enquete (enquete_id, aluno_id)
    VALUES (p_enquete_id, p_aluno_id);

    FOREACH v_opcao_id IN ARRAY p_opcoes_ids
    LOOP
        IF NOT EXISTS (SELECT 1 FROM opcoes_enquete WHERE id = v_opcao_id AND enquete_id = p_enquete_id) THEN
            RAISE EXCEPTION 'Opção % inválida para a enquete', v_opcao_id;
        END IF;

        UPDATE opcoes_enquete
        SET contador = contador + 1
        WHERE id = v_opcao_id;
    END LOOP;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
"""

def init_db():
    """
    Inicializa as tabelas do banco de dados no Supabase.
    ATENÇÃO: Em produção, recomenda-se executar essas migrações diretamente 
    pelo SQL Editor do painel do Supabase. Este script é apenas um facilitador 
    para o ambiente de desenvolvimento local.
    """
    print("Inicializando tabelas do banco de dados (Módulo Desafios e Mini-Provas)...")
    
    # Obtém a instância do provider para acessar a configuração
    db_provider = ProviderFactory.create("supabase")
    
    # Como não temos uma função RPC nativa genérica de `execute_sql` por padrão
    # no pacote supabase-py para strings DDL completas, a forma mais garantida
    # é criar as tabelas via REST se não der erro, ou pedir que o usuário
    # execute no SQL Editor.
    
    print("\n" + "="*80)
    print("Por favor, execute o script SQL abaixo no SQL Editor do seu projeto Supabase:")
    print("Isso garantirá a criação correta de todas as tabelas e chaves estrangeiras.")
    print("="*80 + "\n")
    print(SCHEMA_SQL)
    print("\n" + "="*80 + "\n")
    
    # Se o projeto Supabase tiver uma função 'exec_sql' RPC criada, poderíamos chamá-á:
    # try:
    #     db_provider.client.rpc("exec_sql", {"sql_query": SCHEMA_SQL}).execute()
    # except Exception as e:
    #     logger.warning(f"Não foi possível rodar o SQL via RPC. Execute no painel do Supabase. Erro: {e}")

if __name__ == "__main__":
    init_db()
