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
        st.error(f"Erro ao carregar provas: {e}")
        return []

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
    turma_id = st.session_state.get("turma_id")
    
    if "questoes_nova_prova" not in st.session_state:
        st.session_state.questoes_nova_prova = []

    with st.container(border=True):
        titulo = st.text_input("Título da Prova")
        tempo_limite = st.number_input("Tempo Limite (segundos)", min_value=60, max_value=3600, value=300)
        
        st.write("### Questões")
        
        for i, q in enumerate(st.session_state.questoes_nova_prova):
            with st.expander(f"Questão {i+1} - {q['enunciado'][:30]}..."):
                for alt in q['alternativas']:
                    correta_mark = "✅" if alt['correta'] else ""
                    st.write(f"{alt['letra']}: {alt['texto']} {correta_mark}")
                st.write(f"Pontos: {q['pontuacao']}")
                
        if st.button("➕ Adicionar Nova Questão"):
            st.session_state.nova_questao_modal = True
            st.rerun()
            
        if st.session_state.get("nova_questao_modal", False):
            with st.form("form_nova_questao"):
                st.write("Nova Questão")
                enunc = st.text_area("Enunciado")
                alt_a = st.text_input("Alternativa A")
                alt_b = st.text_input("Alternativa B")
                alt_c = st.text_input("Alternativa C")
                alt_d = st.text_input("Alternativa D")
                correta = st.selectbox("Alternativa Correta", ["A", "B", "C", "D"])
                pontos_q = st.number_input("Pontos", min_value=1, value=10)
                
                if st.form_submit_button("Salvar Questão"):
                    st.session_state.questoes_nova_prova.append({
                        "enunciado": enunc,
                        "tipo": "multipla_escolha",
                        "pontuacao": float(pontos_q),
                        "alternativas": [
                            {"letra": "A", "texto": alt_a, "correta": correta == "A"},
                            {"letra": "B", "texto": alt_b, "correta": correta == "B"},
                            {"letra": "C", "texto": alt_c, "correta": correta == "C"},
                            {"letra": "D", "texto": alt_d, "correta": correta == "D"}
                        ]
                    })
                    st.session_state.nova_questao_modal = False
                    st.rerun()
            
        st.divider()
        if st.button("Salvar Mini-Prova", type="primary"):
            if not titulo or not st.session_state.questoes_nova_prova:
                st.error("Preencha o título e adicione pelo menos uma questão.")
            else:
                with st.spinner("Salvando..."):
                    try:
                        api_client.criar_mini_prova({
                            "titulo": titulo,
                            "turma_id": turma_id,
                            "tempo_limite_segundos": tempo_limite,
                            "questoes": st.session_state.questoes_nova_prova
                        })
                        st.success("Prova salva com sucesso!")
                        st.session_state.questoes_nova_prova = []
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao criar prova: {e}")

def tela_aluno():
    st.subheader("📝 Suas Provas Disponíveis")
    turma_id = st.session_state.get("turma_id")
    provas = carregar_provas(turma_id)
    
    if not provas:
        st.info("Você não tem mini-provas disponíveis no momento.")
        return
        
    if "prova_em_andamento" not in st.session_state:
        for p in provas:
            with st.container(border=True):
                col1, col2 = st.columns([3,1])
                col1.markdown(f"**{p.get('titulo')}**")
                col1.write(f"⏱️ Tempo Limite: {p.get('duracao_segundos', 300) // 60} minutos")
                if col2.button("Iniciar Prova", key=f"btn_iniciar_{p.get('id')}", type="primary"):
                    try:
                        prova_completa = api_client.obter_prova_detalhes(p.get('id'))
                        tentativa = api_client.iniciar_tentativa(p.get('id'))
                        st.session_state.prova_em_andamento = prova_completa
                        st.session_state.tentativa_id = tentativa.get("id")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao iniciar prova: {e}")
    else:
        prova = st.session_state.prova_em_andamento
        tentativa_id = st.session_state.tentativa_id
        st.info("⚠️ A prova começou! Não recarregue a página (F5) ou feche a aba, o tempo está correndo no servidor.")
        st.markdown(f"### {prova.get('titulo')}")
        
        # Injeta o cronômetro visual em JS
        js_timer(prova.get('duracao_segundos', 300))
        
        with st.form("form_prova"):
            respostas = {}
            for q in prova.get('questoes', []):
                st.markdown(f"**{q.get('enunciado')}**")
                
                # Extrai as alternativas da lista de dicionários
                alternativas_list = q.get('alternativas', [])
                if alternativas_list:
                    labels = [f"{alt.get('letra')}) {alt.get('texto')}" for alt in alternativas_list]
                    escolha = st.radio("Selecione a alternativa:", labels, key=f"q_{q.get('id')}", index=None)
                    if escolha:
                        respostas[q.get('id')] = escolha[0] # Pega a letra (primeiro caractere)
                else:
                    st.info("Questão sem alternativas.")
                st.write("---")
                
            if st.form_submit_button("Submeter Respostas", type="primary"):
                # Converter dict para array
                lista_respostas = [{"questao_id": k, "alternativa_assinalada": v} for k, v in respostas.items()]
                with st.spinner("Enviando..."):
                    try:
                        api_client.responder_tentativa(tentativa_id, lista_respostas)
                        st.success("Respostas enviadas com sucesso! Sua nota foi calculada.")
                        del st.session_state.prova_em_andamento
                        del st.session_state.tentativa_id
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao submeter: {e}")
                    
        if st.button("Cancelar e Sair (A tentativa não será salva)"):
            del st.session_state.prova_em_andamento
            del st.session_state.tentativa_id
            st.rerun()


def main():
    check_login()
    role = st.session_state.user.get("role", "aluno")
    
    st.title("📝 Mini-Provas")
    
    if not st.session_state.get("turma_id"):
        st.warning("Você não está vinculado a nenhuma turma.")
        return
        
    if role == "professor":
        tela_professor()
    elif role == "aluno":
        tela_aluno()

if __name__ == "__main__":
    main()
