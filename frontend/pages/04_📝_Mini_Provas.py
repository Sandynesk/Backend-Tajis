import streamlit as st
import streamlit.components.v1 as components
from utils import check_login
import api_client
import json

st.set_page_config(page_title="Mini-Provas - TAJI", page_icon="📝")

def carregar_provas(turma_id):
    try:
        provas = api_client.listar_mini_provas_turma(turma_id)
        return provas
    except Exception as e:
        return [
            {"id": 1, "titulo": "Quiz de Revisão Python", "tempo_limite": 300, "status": "disponivel", "questoes": [{"id": 1, "enunciado": "O que é uma tupla?", "alternativas": [{"id": "a", "texto": "Lista imutável"}, {"id": "b", "texto": "Um erro de sintaxe"}]}]}
        ]

def js_timer(tempo_segundos):
    """
    Renderiza um cronômetro regressivo em HTML/JS puro para não travar a UI do Streamlit.
    """
    timer_html = f"""
    <div id="timer" style="font-family: sans-serif; font-size: 24px; font-weight: bold; color: #E53E3E; text-align: center; padding: 10px; background: #FED7D7; border-radius: 8px; width: 150px; margin: 0 auto;">
        Carregando...
    </div>
    <script>
        var timeLeft = {tempo_segundos};
        var timerEl = document.getElementById("timer");
        var interval = setInterval(function() {{
            if(timeLeft <= 0) {{
                clearInterval(interval);
                timerEl.innerHTML = "TEMPO ESGOTADO!";
                timerEl.style.background = "#9B2C2C";
                timerEl.style.color = "white";
                // Idealmente, poderíamos acionar um submit do form pai aqui via postMessage,
                // mas como o backend já rejeita, apenas avisamos o usuário.
            }} else {{
                var m = Math.floor(timeLeft / 60);
                var s = timeLeft % 60;
                timerEl.innerHTML = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                timeLeft--;
            }}
        }}, 1000);
    </script>
    """
    components.html(timer_html, height=70)


def tela_professor():
    st.subheader("📝 Criar Mini-Prova")
    
    if "questoes_nova_prova" not in st.session_state:
        st.session_state.questoes_nova_prova = []

    with st.container(border=True):
        titulo = st.text_input("Título da Prova")
        desc = st.text_area("Descrição")
        tempo_limite = st.number_input("Tempo Limite (segundos)", min_value=60, max_value=3600, value=300)
        turma = st.selectbox("Turma", ["Turma A", "Turma B"])
        
        st.write("### Questões")
        
        for i, q in enumerate(st.session_state.questoes_nova_prova):
            with st.expander(f"Questão {i+1} - {q['enunciado'][:30]}..."):
                st.write(q)
                
        if st.button("➕ Adicionar Nova Questão"):
            st.session_state.questoes_nova_prova.append({
                "enunciado": "Nova Questão",
                "tipo": "multipla_escolha",
                "alternativas": []
            })
            st.rerun()
            
        st.divider()
        if st.button("Salvar Mini-Prova", type="primary"):
            with st.spinner("Salvando..."):
                st.success("Prova salva com sucesso! (Mock)")
                st.session_state.questoes_nova_prova = []
                st.rerun()

def tela_aluno():
    st.subheader("📝 Suas Provas Disponíveis")
    
    # Mock
    turma_id_mock = 1
    provas = carregar_provas(turma_id_mock)
    
    if "prova_em_andamento" not in st.session_state:
        for p in provas:
            with st.container(border=True):
                col1, col2 = st.columns([3,1])
                col1.markdown(f"**{p['titulo']}**")
                col1.write(f"⏱️ Tempo Limite: {p['tempo_limite'] // 60} minutos")
                if col2.button("Iniciar Prova", key=f"btn_iniciar_{p['id']}", type="primary"):
                    st.session_state.prova_em_andamento = p
                    st.rerun()
    else:
        prova = st.session_state.prova_em_andamento
        st.info("⚠️ A prova começou! Não recarregue a página (F5) ou feche a aba, o tempo está correndo no servidor.")
        st.markdown(f"### {prova['titulo']}")
        
        # Injeta o cronômetro visual em JS
        js_timer(prova['tempo_limite'])
        
        with st.form("form_prova"):
            respostas = {}
            for q in prova.get('questoes', []):
                st.markdown(f"**{q['enunciado']}**")
                opcoes = [alt['texto'] for alt in q['alternativas']]
                resposta_selecionada = st.radio("Selecione a alternativa correta:", opcoes, key=f"q_{q['id']}")
                respostas[q['id']] = resposta_selecionada
                st.write("---")
                
            if st.form_submit_button("Submeter Respostas", type="primary"):
                with st.spinner("Enviando..."):
                    st.success("Respostas enviadas com sucesso! Sua nota foi calculada. (Mock)")
                    del st.session_state.prova_em_andamento
                    st.rerun()
                    
        if st.button("Cancelar e Sair (A tentativa não será salva)"):
            del st.session_state.prova_em_andamento
            st.rerun()


def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("📝 Mini-Provas")
    
    if role == "professor":
        tela_professor()
    elif role == "aluno":
        tela_aluno()

if __name__ == "__main__":
    main()
