import streamlit as st
from utils import check_login
import api_client

st.set_page_config(page_title="Missões - TAJI", page_icon="🎯")

def carregar_missoes(turma_id):
    try:
        return api_client.listar_missoes_turma(turma_id)
    except Exception as e:
        st.error(f"Erro ao carregar missões: {e}")
        return []

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("🎯 Missões")
    
    turma_id = st.session_state.get("turma_id")
    if not turma_id:
        st.warning("Você não está vinculado a nenhuma turma.")
        return
    
    if role == "professor":
        with st.expander("➕ Criar Nova Missão"):
            with st.form("form_nova_missao"):
                titulo = st.text_input("Título da Missão")
                desc = st.text_area("Descrição")
                # No MVP simplificado, a criação só pede titulo e descricao. Recompensa fica por etapa.
                
                if st.form_submit_button("Criar Missão"):
                    with st.spinner("Salvando..."):
                        try:
                            api_client.api_request("POST", "/missoes/", data={
                                "titulo": titulo,
                                "descricao": desc,
                                "turma_id": turma_id
                            })
                            st.success("Missão criada!")
                        except Exception as e:
                            st.error(f"Erro ao criar missão: {e}")
                    
        st.subheader("Missões Ativas da Turma")
        missoes = carregar_missoes(turma_id)
        if not missoes:
            st.info("Nenhuma missão criada ainda.")
        for m in missoes:
            st.write(f"- **{m.get('titulo')}**: {m.get('descricao')}")
            
    elif role == "aluno":
        st.subheader("Trilhas de Aprendizagem")
        missoes = carregar_missoes(turma_id)
        
        if not missoes:
            st.info("Nenhuma trilha de aprendizagem disponível no momento.")
            
        for m in missoes:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"### {m.get('titulo')}")
                col1.write(m.get('descricao'))
                
                # Try to get status
                # Na API atual, missoes são listadas globalmente e progresso é buscado
                # Como simplificação do MVP, apenas deixamos a missão "disponível"
                if col2.button("Detalhes da Missão", key=f"btn_detalhes_{m.get('id')}"):
                    st.info("Visualização de etapas de missão ainda não implementada neste MVP.")

if __name__ == "__main__":
    main()
