import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Gamificação - TAJI", page_icon="🏆")

def carregar_ranking():
    try:
        return api_client.get_ranking_geral()
    except Exception as e:
        return [
            {"posicao": 1, "nome": "Maria Silva", "pontos": 3500, "nivel": 10},
            {"posicao": 2, "nome": "João Pedro", "pontos": 3200, "nivel": 9},
            {"posicao": 3, "nome": "Ana Costa", "pontos": 2800, "nivel": 8},
            {"posicao": 4, "nome": "Seu Nome (Mock)", "pontos": 1250, "nivel": 5}
        ]

def carregar_medalhas():
    try:
        return api_client.get_medalhas_aluno(st.session_state.user['id'])
    except Exception as e:
        return [
            {"nome": "Primeiro Sangue", "icone": "🩸", "descricao": "Completou o primeiro desafio."},
            {"nome": "Veloz e Furioso", "icone": "🏎️", "descricao": "Respondeu a prova em tempo recorde."}
        ]

def main():
    check_login()
    
    st.title("🏆 Gamificação")
    
    tab1, tab2, tab3 = st.tabs(["Meu Progresso", "Ranking Geral", "Minhas Medalhas"])
    
    with tab1:
        st.subheader("Seu Status Atual")
        # Simulação de progresso de nível
        nivel_atual = 5
        pontos_atuais = 1250
        pontos_prox_nivel = 1500
        
        st.markdown(f"**Nível {nivel_atual}**")
        progresso = pontos_atuais / pontos_prox_nivel
        st.progress(progresso, text=f"{pontos_atuais} / {pontos_prox_nivel} XP para o Nível {nivel_atual + 1}")
        
    with tab2:
        st.subheader("Top 50 - Ranking Global")
        ranking = carregar_ranking()
        if ranking:
            df = pd.DataFrame(ranking)
            # Destaque se o aluno não estiver no top (mock simples)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    with tab3:
        st.subheader("Galeria de Conquistas")
        medalhas = carregar_medalhas()
        if medalhas:
            cols = st.columns(3)
            for i, m in enumerate(medalhas):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"<h1 style='text-align: center;'>{m['icone']}</h1>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style='text-align: center;'>{m['nome']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; color: gray;'>{m['descricao']}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
