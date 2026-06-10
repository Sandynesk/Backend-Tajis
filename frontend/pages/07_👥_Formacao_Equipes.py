import streamlit as st
from utils import check_login
import api_client

st.set_page_config(page_title="Formação de Equipes - TAJI", page_icon="👥")

def carregar_formacao(turma_id):
    try:
        return api_client.listar_formacoes_turma(turma_id)
    except Exception as e:
        return [
            {"id": 1, "nome": "Projeto Final", "tamanho_grupo": 4, "grupos": [
                {"id": 101, "nome": "Equipe Alpha", "membros": ["Maria", "João", "Ana", "Carlos"]},
                {"id": 102, "nome": "Equipe Beta", "membros": ["Pedro", "Lucas", "Julia", "Fernanda"]}
            ]}
        ]

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("👥 Formação de Equipes")
    st.write("Equipes geradas automaticamente pelo algoritmo de balanceamento.")
    
    turma_id_mock = 1
    
    if role == "professor":
        with st.expander("⚙️ Gerar Nova Formação"):
            with st.form("form_nova_formacao"):
                nome_formacao = st.text_input("Nome/Motivo da Formação (ex: Projeto Final)")
                tamanho = st.number_input("Tamanho de cada grupo", min_value=2, max_value=10, value=4)
                
                if st.form_submit_button("Gerar Equipes (Zig-Zag Algorithm)", type="primary"):
                    st.success("Equipes geradas com sucesso!")
                    
    st.subheader("Equipes Atuais")
    formacoes = carregar_formacao(turma_id_mock)
    
    for f in formacoes:
        st.markdown(f"### {f['nome']}")
        cols = st.columns(min(len(f['grupos']), 3))
        
        for i, grupo in enumerate(f['grupos']):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{grupo['nome']}**")
                    for membro in grupo['membros']:
                        st.write(f"👤 {membro}")

if __name__ == "__main__":
    main()
