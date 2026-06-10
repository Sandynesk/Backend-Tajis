import streamlit as st
from utils import check_login
import api_client

st.set_page_config(page_title="Missões - TAJI", page_icon="🎯")

def carregar_missoes(turma_id):
    try:
        return api_client.listar_missoes_turma(turma_id)
    except Exception as e:
        return [
            {"id": 1, "titulo": "Mestre dos Arrays", "descricao": "Complete 3 desafios sobre arrays.", "pontos_recompensa": 500, "status": "disponivel"},
            {"id": 2, "titulo": "Sobrevivente", "descricao": "Tire nota máxima em uma mini-prova.", "pontos_recompensa": 300, "status": "em_andamento"}
        ]

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("🎯 Missões")
    
    turma_id_mock = 1
    
    if role == "professor":
        with st.expander("➕ Criar Nova Missão"):
            with st.form("form_nova_missao"):
                st.write("Configuração da Missão (Mock)")
                titulo = st.text_input("Título da Missão")
                desc = st.text_area("Descrição")
                pontos = st.number_input("Recompensa (XP)", min_value=50, step=50)
                
                if st.form_submit_button("Criar Missão"):
                    st.success("Missão criada!")
                    
        st.subheader("Missões Ativas da Turma")
        missoes = carregar_missoes(turma_id_mock)
        for m in missoes:
            st.write(f"- **{m['titulo']}**: {m['descricao']} ({m['pontos_recompensa']} XP)")
            
    elif role == "aluno":
        st.subheader("Trilhas de Aprendizagem")
        missoes = carregar_missoes(turma_id_mock)
        
        for m in missoes:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"### {m['titulo']}")
                col1.write(m['descricao'])
                
                if m['status'] == "disponivel":
                    if col2.button("Iniciar Missão", key=f"btn_iniciar_{m['id']}", type="primary"):
                        st.success("Missão Iniciada!")
                elif m['status'] == "em_andamento":
                    col2.info("Em andamento")
                    # Barra de progresso mock
                    st.progress(0.33, "1 / 3 desafios concluídos")

if __name__ == "__main__":
    main()
