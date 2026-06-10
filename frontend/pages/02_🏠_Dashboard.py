import streamlit as st
from utils import check_login, logout, inject_css
from components.ui import xp_bar, stat_card, divider
import api_client

st.set_page_config(page_title="Dashboard - TAJI", page_icon="🏠", layout="wide")
inject_css()

def carregar_dados_aluno():
    try:
        progresso = api_client.get_progresso_aluno(st.session_state.user['id'])
        return progresso
    except Exception as e:
        # st.warning("Usando dados de demonstração – API não encontrada.")
        return {
            "pontuacao": 1250,
            "nivel": 5,
            "desafios_completos": 12,
            "missoes_ativas": 2
        }

def carregar_dados_professor():
    try:
        turmas = api_client.listar_turmas_professor()
        return turmas
    except Exception as e:
        return [
            {"id": 1, "nome": "Programação Web - Turma A", "alunos_count": 35},
            {"id": 2, "nome": "Estrutura de Dados", "alunos_count": 40}
        ]

def main():
    check_login()

    user = st.session_state.user
    role = user.get("role", "aluno")

    st.sidebar.title(f"Olá, {user.get('nome', 'Usuário')} 👋")
    st.sidebar.write(f"**Perfil:** {role.capitalize()}")
    if st.sidebar.button("Sair", type="secondary"):
        logout()

    st.title("🏠 Dashboard")

    if role == "aluno":
        st.subheader("Seu Progresso")
        dados = carregar_dados_aluno()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(stat_card("Pontuação Total", f"{dados.get('pontuacao', 0)} XP", delta="↑ Nível subiu"), unsafe_allow_html=True)
        with col2:
            st.markdown(stat_card("Nível Atual", str(dados.get('nivel', 1))), unsafe_allow_html=True)
        with col3:
            st.markdown(stat_card("Desafios", str(dados.get('desafios_completos', 0))), unsafe_allow_html=True)
        with col4:
            st.markdown(stat_card("Missões Ativas", str(dados.get('missoes_ativas', 0))), unsafe_allow_html=True)
        
        st.markdown(divider("progresso da temporada"), unsafe_allow_html=True)
        # XP para o próximo nível (mock 3000)
        xp_atual = dados.get('pontuacao', 0)
        xp_prox = max(3000, xp_atual + 500)
        st.markdown(xp_bar(xp_atual=xp_atual, xp_proximo=xp_prox, nivel=dados.get('nivel', 1)), unsafe_allow_html=True)
        
        st.write("Use o menu lateral para navegar entre Desafios, Provas e Missões.")

    elif role == "professor":
        st.subheader("Suas Turmas")
        turmas = carregar_dados_professor()
        
        if not turmas:
            st.info("Você ainda não possui turmas cadastradas.")
        else:
            cols = st.columns(min(len(turmas), 3))
            for i, turma in enumerate(turmas):
                with cols[i % 3]:
                    st.card_container = st.container(border=True)
                    st.card_container.markdown(f"### {turma['nome']}")
                    st.card_container.write(f"👥 {turma.get('alunos_count', 0)} alunos")
                    if st.card_container.button("Gerenciar Turma", key=f"btn_{turma['id']}"):
                        st.info("Navegação para gerenciamento da turma ainda a ser implementada.")
                        
        st.divider()
        st.write("Use o menu lateral para criar novos desafios, provas e missões para suas turmas.")

if __name__ == "__main__":
    main()
