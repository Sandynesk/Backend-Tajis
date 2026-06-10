import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Desafios - TAJI", page_icon="📚")

def carregar_desafios(turma_id):
    try:
        desafios = api_client.listar_desafios_turma(turma_id)
        return desafios
    except Exception as e:
        return [
            {"id": 1, "titulo": "Desafio de Lógica", "descricao": "Resolva o problema da Torre de Hanói em Python.", "pontos": 100, "status": "ativo"},
            {"id": 2, "titulo": "Criação de API", "descricao": "Crie um endpoint com FastAPI.", "pontos": 250, "status": "pendente"}
        ]

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("📚 Desafios")

    # Mock turma_id (na prática, o professor escolheria ou pegaria da sessão)
    turma_id_mock = 1

    if role == "professor":
        with st.expander("➕ Criar Novo Desafio"):
            with st.form("form_novo_desafio"):
                titulo = st.text_input("Título do Desafio")
                desc = st.text_area("Descrição")
                pontos = st.number_input("Pontuação (XP)", min_value=10, max_value=1000, step=10)
                turma = st.selectbox("Turma", ["Turma A", "Turma B"]) # Mock
                
                if st.form_submit_button("Criar Desafio", type="primary"):
                    with st.spinner("Salvando..."):
                        try:
                            api_client.criar_desafio({
                                "titulo": titulo,
                                "descricao": desc,
                                "pontos": pontos,
                                "turma_id": turma_id_mock
                            })
                            st.success("Desafio criado com sucesso!")
                        except Exception as e:
                            st.warning("Mock: Desafio criado com sucesso!")

        st.subheader("Desafios Cadastrados")
        desafios = carregar_desafios(turma_id_mock)
        if desafios:
            df = pd.DataFrame(desafios)
            st.dataframe(df, use_container_width=True, hide_index=True)

    elif role == "aluno":
        st.subheader("Seus Desafios")
        desafios = carregar_desafios(turma_id_mock)
        
        for d in desafios:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"### {d['titulo']}")
                col1.write(d['descricao'])
                col2.metric("Recompensa", f"{d['pontos']} XP")
                col2.button("Visualizar Detalhes", key=f"btn_desc_{d['id']}")

if __name__ == "__main__":
    main()
