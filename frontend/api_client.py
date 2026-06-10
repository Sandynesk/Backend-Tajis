import os
import requests
import streamlit as st
from requests.exceptions import RequestException, Timeout

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def handle_401():
    """Lida com token expirado ou inválido limpando a sessão e forçando recarregamento."""
    st.session_state.clear()
    st.warning("Sua sessão expirou. Por favor, faça login novamente.")
    st.rerun()

def api_request(method, endpoint, data=None, params=None):
    """
    Função genérica para fazer requisições à API.
    Injeta o token automaticamente se existir.
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
        
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, params=params, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, params=params, timeout=10)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data, params=params, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, params=params, timeout=10)
        else:
            raise ValueError(f"Método HTTP não suportado: {method}")

        if response.status_code == 401:
            handle_401()
            return None # Nunca vai chegar aqui devido ao st.rerun()

        # Tentar ler o JSON
        try:
            json_data = response.json()
        except ValueError:
            json_data = None
            
        if not response.ok:
            error_detail = json_data.get("detail", "Erro desconhecido") if json_data else response.text
            raise Exception(f"{response.status_code} - {error_detail}")
            
        return json_data

    except Timeout:
        raise Exception("Timeout: A API demorou muito para responder.")
    except RequestException as e:
        raise Exception(f"Erro de conexão: Não foi possível conectar à API.")

# ---- Funções Específicas ----

def login(email, senha):
    return api_request("POST", "/auth/login", data={"email": email, "senha": senha})

def register_aluno(data):
    return api_request("POST", "/auth/register/aluno", data=data)

def register_professor(data):
    return api_request("POST", "/auth/register/professor", data=data)

# Desafios
def listar_desafios_turma(turma_id):
    return api_request("GET", f"/desafios/turma/{turma_id}")

def criar_desafio(data):
    return api_request("POST", "/desafios", data=data)

# Mini-Provas
def listar_mini_provas_turma(turma_id):
    return api_request("GET", f"/mini-provas/turma/{turma_id}")

def criar_mini_prova(data):
    return api_request("POST", "/mini-provas", data=data)

def iniciar_tentativa(prova_id):
    return api_request("POST", f"/mini-provas/{prova_id}/iniciar")

def responder_tentativa(tentativa_id, respostas):
    return api_request("POST", f"/tentativas/{tentativa_id}/responder", data=respostas)

# Enquetes
def listar_enquetes_turma(turma_id):
    return api_request("GET", f"/enquetes/turma/{turma_id}")

def criar_enquete(data):
    return api_request("POST", "/enquetes", data=data)

def votar_enquete(enquete_id, opcoes):
    return api_request("POST", f"/enquetes/{enquete_id}/votar", data={"opcoes": opcoes})

# Gamificação
def get_ranking_geral():
    return api_request("GET", "/gamificacao/ranking")

def get_ranking_semanal():
    return api_request("GET", "/gamificacao/ranking/semanal")

def get_medalhas_aluno(aluno_id):
    return api_request("GET", f"/gamificacao/medalhas/{aluno_id}")

def get_progresso_aluno(aluno_id):
    return api_request("GET", f"/gamificacao/progresso/{aluno_id}")

# Missões
def listar_missoes_turma(turma_id):
    return api_request("GET", f"/missoes/turma/{turma_id}")

def iniciar_missao(missao_id):
    return api_request("POST", f"/missoes/{missao_id}/iniciar")

def criar_missao(data):
    return api_request("POST", "/missoes", data=data)

# Formação de Equipes
def listar_formacoes_turma(turma_id):
    return api_request("GET", f"/formacao/turma/{turma_id}")

def criar_formacao(data):
    return api_request("POST", "/formacao", data=data)

# Turmas
def listar_turmas_professor():
    return api_request("GET", "/turmas/minhas")
