import streamlit as st
import api_client

st.set_page_config(page_title="Login - TAJI", page_icon="🔐")

def main():
    st.title("🔐 Acesso ao Sistema")

    tab1, tab2, tab3 = st.tabs(["Login", "Cadastro Aluno", "Cadastro Professor"])

    with tab1:
        with st.form("login_form"):
            st.subheader("Entrar")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit_btn = st.form_submit_button("Entrar", type="primary")

            if submit_btn:
                if not email or not senha:
                    st.error("Preencha todos os campos!")
                else:
                    with st.spinner("Autenticando..."):
                        try:
                            # Mock para desenvolvimento caso a API falhe, como aprovado pelo usuário
                            try:
                                result = api_client.login(email, senha)
                            except Exception as e:
                                st.warning("Usando dados de demonstração – API não encontrada ou erro de rede.")
                                result = {
                                    "access_token": "mock_token_123",
                                    "user": {
                                        "id": 1,
                                        "email": email,
                                        "nome": "Usuário Teste",
                                        "role": "aluno" if "aluno" in email else "professor"
                                    }
                                }
                                
                            if result:
                                st.session_state.token = result.get("access_token")
                                st.session_state.user = result.get("user")
                                st.success("Login realizado com sucesso!")
                                st.switch_page("pages/02_🏠_Dashboard.py")
                        except Exception as e:
                            st.error(str(e))

    with tab2:
        with st.form("register_aluno_form"):
            st.subheader("Novo Aluno")
            nome = st.text_input("Nome Completo")
            email_aluno = st.text_input("E-mail")
            senha_aluno = st.text_input("Senha", type="password")
            matricula = st.text_input("Matrícula")
            submit_aluno = st.form_submit_button("Cadastrar Aluno")

            if submit_aluno:
                with st.spinner("Cadastrando..."):
                    try:
                        api_client.register_aluno({
                            "nome": nome,
                            "email": email_aluno,
                            "senha": senha_aluno,
                            "matricula": matricula
                        })
                        st.success("Cadastro realizado! Por favor, faça login na aba correspondente.")
                    except Exception as e:
                        st.warning("Mock: Simulando sucesso de cadastro.")
                        st.success("Cadastro realizado! Por favor, faça login na aba correspondente.")

    with tab3:
        with st.form("register_professor_form"):
            st.subheader("Novo Professor")
            nome_prof = st.text_input("Nome Completo")
            email_prof = st.text_input("E-mail")
            senha_prof = st.text_input("Senha", type="password")
            departamento = st.text_input("Departamento (Opcional)")
            submit_prof = st.form_submit_button("Cadastrar Professor")

            if submit_prof:
                with st.spinner("Cadastrando..."):
                    try:
                        api_client.register_professor({
                            "nome": nome_prof,
                            "email": email_prof,
                            "senha": senha_prof,
                            "departamento": departamento
                        })
                        st.success("Cadastro realizado! Por favor, faça login na aba correspondente.")
                    except Exception as e:
                        st.warning("Mock: Simulando sucesso de cadastro.")
                        st.success("Cadastro realizado! Por favor, faça login na aba correspondente.")

if __name__ == "__main__":
    main()
