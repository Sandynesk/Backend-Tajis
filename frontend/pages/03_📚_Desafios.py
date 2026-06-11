import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Desafios - TAJI", page_icon="📚")

@st.dialog("Detalhes do Desafio")
def mostrar_detalhes(desafio):
    st.write(f"**Título:** {desafio.get('titulo')}")
    st.write(f"**Descrição:** {desafio.get('descricao')}")
    st.write(f"**Recompensa:** {desafio.get('pontos')} XP")
    if "status" in desafio:
        st.write(f"**Status:** {desafio.get('status')}")
    
    if st.button("Fechar"):
        st.rerun()

def carregar_desafios(turma_id):
    try:
        desafios = api_client.listar_desafios_turma(turma_id)
        return desafios
    except Exception as e:
        st.error(f"Erro ao carregar desafios: {e}")
        return []

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    turma_id = st.session_state.get("turma_id")
    
    if not turma_id:
        st.warning("Você não está vinculado a nenhuma turma.")
        return
        
    st.title("📚 Desafios")

    if role == "professor":
        with st.expander("➕ Criar Novo Desafio"):
            with st.form("form_novo_desafio"):
                titulo = st.text_input("Título do Desafio")
                desc = st.text_area("Descrição")
                pontos = st.number_input("Pontuação (XP)", min_value=10, max_value=1000, step=10)
                
                if st.form_submit_button("Criar Desafio", type="primary"):
                    with st.spinner("Salvando..."):
                        try:
                            api_client.criar_desafio({
                                "titulo": titulo,
                                "descricao": desc,
                                "pontos": pontos,
                                "turma_id": turma_id
                            })
                            st.success("Desafio criado com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao criar desafio: {e}")

        st.subheader("Desafios Cadastrados")
        desafios = carregar_desafios(turma_id)
        if desafios:
            df = pd.DataFrame(desafios)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum desafio encontrado para esta turma.")

    elif role == "aluno":
        st.subheader("Seus Desafios")
        desafios = carregar_desafios(turma_id)
        
        if not desafios:
            st.info("Você não tem desafios pendentes no momento.")
            
        for d in desafios:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"### {d.get('titulo')}")
                # Exibir apenas um trecho da descrição
                desc_curta = d.get('descricao', '')[:100] + "..." if len(d.get('descricao', '')) > 100 else d.get('descricao', '')
                col1.write(desc_curta)
                col2.metric("Recompensa", f"{d.get('pontos')} XP")
                if col2.button("Visualizar Detalhes", key=f"btn_desc_{d.get('id')}"):
                    mostrar_detalhes(d)

if __name__ == "__main__":
    main()
