import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Enquetes - TAJI", page_icon="📊")

def carregar_enquetes(turma_id):
    try:
        return api_client.listar_enquetes_turma(turma_id)
    except Exception as e:
        return [
            {
                "id": 1, 
                "titulo": "Feedback da Aula 05", 
                "descricao": "O que você achou do ritmo da aula sobre FastAPI?",
                "opcoes": ["Muito rápido", "Adequado", "Muito lento"],
                "resultados": {"Muito rápido": 5, "Adequado": 25, "Muito lento": 2},
                "status": "encerrada"
            },
            {
                "id": 2, 
                "titulo": "Próximo Tópico", 
                "descricao": "Qual assunto devemos aprofundar na revisão?",
                "opcoes": ["Docker", "Deploy", "Testes Unitários"],
                "resultados": {},
                "status": "ativa"
            }
        ]

def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("📊 Enquetes e Feedback")
    turma_id_mock = 1
    
    if role == "professor":
        if "opcoes_nova_enquete" not in st.session_state:
            st.session_state.opcoes_nova_enquete = ["Opção 1"]
            
        with st.expander("➕ Criar Nova Enquete"):
            with st.form("form_nova_enquete"):
                titulo = st.text_input("Título")
                desc = st.text_area("Descrição")
                
                st.write("Opções de Resposta")
                for i, op in enumerate(st.session_state.opcoes_nova_enquete):
                    st.text_input(f"Opção {i+1}", value=op, key=f"op_{i}")
                    
                col_add, col_submit = st.columns([1, 1])
                # Botões de formulário não podem adicionar itens à lista e renderizar imediatamente da melhor forma sem rerun
                # Então fazemos fora do form, ou usamos um form submit que não recarrega. 
                # Streamlit form limitation: st.form_submit_button reseta tudo se não for cuidadoso.
                
                submitted = st.form_submit_button("Lançar Enquete", type="primary")
                if submitted:
                    st.success("Enquete lançada! (Mock)")
                    st.session_state.opcoes_nova_enquete = ["Opção 1"]
                    st.rerun()

        # Botão para adicionar opção (fora do form para não dar submit)
        if st.button("➕ Adicionar Opção"):
            st.session_state.opcoes_nova_enquete.append(f"Nova Opção {len(st.session_state.opcoes_nova_enquete) + 1}")
            st.rerun()

        st.subheader("Resultados das Enquetes")
        enquetes = carregar_enquetes(turma_id_mock)
        for e in enquetes:
            with st.container(border=True):
                st.markdown(f"### {e['titulo']}")
                st.write(e['descricao'])
                if e['resultados']:
                    df = pd.DataFrame({
                        "Opção": list(e['resultados'].keys()),
                        "Votos": list(e['resultados'].values())
                    }).set_index("Opção")
                    st.bar_chart(df)
                else:
                    st.info("Ainda não há votos suficientes para exibir resultados.")

    elif role == "aluno":
        st.subheader("Enquetes Ativas")
        enquetes = carregar_enquetes(turma_id_mock)
        
        for e in enquetes:
            if e['status'] == "ativa":
                with st.container(border=True):
                    st.markdown(f"### {e['titulo']}")
                    st.write(e['descricao'])
                    
                    with st.form(f"form_voto_{e['id']}"):
                        voto = st.radio("Selecione sua resposta:", e['opcoes'])
                        if st.form_submit_button("Votar", type="primary"):
                            st.success("Seu voto foi registrado!")

if __name__ == "__main__":
    main()
