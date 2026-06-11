import streamlit as st
from utils import check_login
import api_client

st.set_page_config(page_title="Formação de Equipes - TAJI", page_icon="👥")

def carregar_formacao(turma_id):
    try:
        return api_client.listar_formacoes_turma(turma_id)
    except Exception as e:
        st.error(f"Erro ao carregar formações: {e}")
        return []

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("👥 Formação de Equipes")
    st.write("Equipes geradas automaticamente pelo algoritmo de balanceamento.")
    
    turma_id = st.session_state.get("turma_id")
    if not turma_id:
        st.warning("Você não está vinculado a nenhuma turma.")
        return
    
    if role == "professor":
        with st.expander("⚙️ Gerar Nova Formação"):
            with st.form("form_nova_formacao"):
                nome_formacao = st.text_input("Nome/Motivo da Formação (ex: Projeto Final)")
                tamanho = st.number_input("Tamanho de cada grupo", min_value=2, max_value=10, value=4)
                
                if st.form_submit_button("Gerar Equipes (Zig-Zag Algorithm)", type="primary"):
                    with st.spinner("Gerando equipes..."):
                        try:
                            # A rota exata depende da implementação no backend, usando gerar_formacao aqui
                            api_client.api_request("POST", "/formacao/gerar", data={
                                "turma_id": turma_id,
                                "nome_formacao": nome_formacao,
                                "tamanho_grupo": tamanho
                            })
                            st.success("Equipes geradas com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao gerar equipes: {e}")
                    
    st.subheader("Equipes Atuais")
    formacoes = carregar_formacao(turma_id)
    
    if not formacoes:
        st.info("Nenhuma equipe foi gerada para esta turma ainda.")
    
    for f in formacoes:
        st.markdown(f"### {f.get('nome', 'Formação')}")
        grupos = f.get('grupos', [])
        if grupos:
            cols = st.columns(min(len(grupos), 3) if len(grupos) > 0 else 1)
            
            for i, grupo in enumerate(grupos):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"**{grupo.get('nome', 'Grupo')}**")
                        for membro in grupo.get('membros', []):
                            # Se membro for dict
                            nome_membro = membro.get("nome") if isinstance(membro, dict) else membro
                            st.write(f"👤 {nome_membro}")
        else:
            st.write("Nenhum grupo encontrado nesta formação.")

if __name__ == "__main__":
    main()
