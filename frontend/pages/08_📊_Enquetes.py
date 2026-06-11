import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Enquetes - TAJI", page_icon="📊")

def carregar_enquetes(turma_id):
    try:
        return api_client.listar_enquetes_turma(turma_id)
    except Exception as e:
        st.error(f"Erro ao carregar enquetes: {e}")
        return []

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("📊 Enquetes e Feedback")
    turma_id = st.session_state.get("turma_id")
    
    if not turma_id:
        st.warning("Você não está vinculado a nenhuma turma.")
        return
    
    if role == "professor":
        if "opcoes_nova_enquete" not in st.session_state:
            st.session_state.opcoes_nova_enquete = ["Opção 1"]
            
        with st.expander("➕ Criar Nova Enquete"):
            with st.form("form_nova_enquete"):
                titulo = st.text_input("Título")
                desc = st.text_area("Descrição (opcional)")
                
                st.write("Opções de Resposta")
                opcoes_informadas = []
                for i, op in enumerate(st.session_state.opcoes_nova_enquete):
                    # Use unique key and capture value
                    val = st.text_input(f"Opção {i+1}", value=op, key=f"op_{i}")
                    opcoes_informadas.append(val)
                    
                submitted = st.form_submit_button("Lançar Enquete", type="primary")
                if submitted:
                    opcoes_validas = [o for o in opcoes_informadas if o.strip()]
                    if not titulo or len(opcoes_validas) < 2:
                        st.error("Preencha o título e pelo menos 2 opções.")
                    else:
                        with st.spinner("Lançando enquete..."):
                            try:
                                api_client.api_request("POST", "/enquetes/", data={
                                    "titulo": titulo,
                                    "turma_id": turma_id,
                                    "opcoes": opcoes_validas
                                })
                                st.success("Enquete lançada!")
                                st.session_state.opcoes_nova_enquete = ["Opção 1"]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao lançar enquete: {e}")

        # Botão para adicionar opção (fora do form para não dar submit)
        if st.button("➕ Adicionar Opção"):
            st.session_state.opcoes_nova_enquete.append(f"Nova Opção {len(st.session_state.opcoes_nova_enquete) + 1}")
            st.rerun()

        st.subheader("Resultados das Enquetes")
        enquetes = carregar_enquetes(turma_id)
        if not enquetes:
            st.info("Nenhuma enquete cadastrada.")
        for e in enquetes:
            with st.container(border=True):
                st.markdown(f"### {e.get('titulo')}")
                st.write(e.get('descricao', ''))
                resultados = e.get('resultados', {})
                if resultados:
                    df = pd.DataFrame({
                        "Opção": list(resultados.keys()),
                        "Votos": list(resultados.values())
                    }).set_index("Opção")
                    st.bar_chart(df)
                else:
                    st.info("Ainda não há votos suficientes para exibir resultados.")

    elif role == "aluno":
        st.subheader("Enquetes Ativas")
        enquetes = carregar_enquetes(turma_id)
        
        ativas = [e for e in enquetes if e.get('ativa', True)]
        if not ativas:
            st.info("Nenhuma enquete ativa no momento.")
            
        for e in ativas:
            with st.container(border=True):
                st.markdown(f"### {e.get('titulo')}")
                st.write(e.get('descricao', ''))
                
                opcoes = e.get('opcoes', [])
                if opcoes:
                    with st.form(f"form_voto_{e.get('id')}"):
                        # Se opcoes for lista de strings ou lista de dicts
                        nomes_opcoes = [op.get('texto') if isinstance(op, dict) else op for op in opcoes]
                        voto = st.radio("Selecione sua resposta:", nomes_opcoes)
                        if st.form_submit_button("Votar", type="primary"):
                            with st.spinner("Enviando..."):
                                try:
                                    # Para o MVP assumimos que votar_enquete recebe opcao como string ou ID
                                    api_client.api_request("POST", f"/enquetes/{e.get('id')}/votar", data={"opcao": voto})
                                    st.success("Seu voto foi registrado!")
                                except Exception as err:
                                    st.error(f"Erro ao votar: {err}")
                else:
                    st.warning("Esta enquete não possui opções.")

if __name__ == "__main__":
    main()
