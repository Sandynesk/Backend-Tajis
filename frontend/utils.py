import streamlit as st
from pathlib import Path

def check_login():
    """Verifica se o usuário está logado. Se não, redireciona para a página de login."""
    if "token" not in st.session_state or not st.session_state.token:
        st.warning("Por favor, faça login para acessar esta página.")
        st.switch_page("pages/01_🔐_Login.py")
        st.stop() # Interrompe a execução da página atual

def logout():
    """Limpa a sessão do usuário e redireciona para a tela inicial (login)."""
    st.session_state.clear()
    st.switch_page("app.py")

def handle_api_error(error_msg):
    """Exibe erro de API de forma padronizada."""
    st.error(f"Erro de comunicação com a API: {error_msg}")

def inject_css() -> None:
    """Injeta o CSS do tema Dark Premium."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {css_path}")
