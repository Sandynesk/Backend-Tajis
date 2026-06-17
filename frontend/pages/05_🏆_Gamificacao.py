import streamlit as st
import pandas as pd
from utils import check_login
import api_client

st.set_page_config(page_title="Gamificação - TAJI", page_icon="🏆")

def carregar_ranking():
    try:
        return api_client.get_ranking_geral()
    except Exception as e:
        st.error(f"Erro ao carregar ranking: {e}")
        return []

def carregar_medalhas():
    try:
        return api_client.get_medalhas_aluno(st.session_state.user['id'])
    except Exception as e:
        st.error(f"Erro ao carregar medalhas: {e}")
        return []

def carregar_progresso():
    try:
        # Assuming the backend returns level, points, etc. or we use st.session_state.user
        # For MVP we can just fetch from an endpoint or use the user session if it has it.
        # But wait, there is get_progresso_aluno in api_client!
        return api_client.get_progresso_aluno(st.session_state.user['id'])
    except Exception as e:
        # st.error(f"Erro ao carregar progresso: {e}") # Silent error if not implemented
        return None

def main():
    check_login()
    
    st.title("🏆 Gamificação")
    
    tab1, tab2, tab3 = st.tabs(["Meu Progresso", "Ranking Geral", "Minhas Medalhas"])
    
    with tab1:
        st.subheader("Seu Status Atual")
        progresso_aluno = carregar_progresso()
        if progresso_aluno:
            nivel_atual = progresso_aluno.get("nivel", 1)
            pontos_atuais = progresso_aluno.get("pontuacao", 0)
            pontos_prox_nivel = progresso_aluno.get("xp_proximo_nivel", pontos_atuais + 1000) # Fallback
            
            st.markdown(f"**Nível {nivel_atual}**")
            # Protect against division by zero or > 1.0 progress
            if pontos_prox_nivel > 0:
                progresso = min(pontos_atuais / pontos_prox_nivel, 1.0)
            else:
                progresso = 1.0
            st.progress(progresso, text=f"{pontos_atuais} / {pontos_prox_nivel} XP para o Nível {nivel_atual + 1}")
        else:
            st.info("Informações de progresso não disponíveis ou não implementadas no momento.")
            # Fallback if API is missing or fails
            user = st.session_state.get("user", {})
            st.markdown(f"**Usuário:** {user.get('nome')}")
            st.markdown(f"**Email:** {user.get('email')}")
        
    with tab2:
        st.subheader("Top 50 - Ranking Global")
        ranking = carregar_ranking()
        if ranking:
            df = pd.DataFrame(ranking)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado de ranking encontrado.")
            
    with tab3:
        st.subheader("Galeria de Conquistas")
        medalhas = carregar_medalhas()
        if medalhas:
            cols = st.columns(3)
            for i, m in enumerate(medalhas):
                with cols[i % 3]:
                    with st.container(border=True):
                        icone = m.get('icone_url') or "🏅"
                        st.markdown(f"<h1 style='text-align: center;'>{icone}</h1>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style='text-align: center;'>{m.get('nome')}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; color: gray;'>{m.get('descricao')}</p>", unsafe_allow_html=True)
        else:
            st.info("Você ainda não possui nenhuma medalha.")

if __name__ == "__main__":
    main()
