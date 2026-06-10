import streamlit as st

st.set_page_config(
    page_title="TAJI - Bem-vindo",
    page_icon="🎓",
    layout="centered"
)

def main():
    st.title("🎓 Bem-vindo ao Sistema TAJI")
    st.write("Plataforma de Engajamento e Gamificação Educacional")

    # Verifica se já existe um token na sessão
    if "token" in st.session_state and st.session_state.token:
        st.success("Você já está logado! Redirecionando para o Dashboard...")
        st.switch_page("pages/02_🏠_Dashboard.py")
    else:
        st.info("Para continuar, por favor faça login ou crie uma conta.")
        if st.button("Ir para Login", type="primary"):
            st.switch_page("pages/01_🔐_Login.py")

if __name__ == "__main__":
    main()
