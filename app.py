import streamlit as st
import google.generativeai as genai

# 1. Configuração Visual da Página (Escondendo os menus do Streamlit)
st.set_page_config(page_title="SMT Expert AI", page_icon="🧠", layout="centered")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Configurando a Chave de API de forma 100% segura
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. O Cérebro do Engenheiro Chefe
instrucao = """
Você é um Engenheiro Especialista SMT em Manaus com 20 anos de experiência. 
Ajude os técnicos a resolverem paradas de linha. Responda de forma muito prática, 
curta e com marcadores. Foque em máquinas Fuji, Panasonic, DEK, Heller, Koh Young. 
Se um erro for mencionado, dê 3 passos práticos para resolver.
"""
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instrucao)

# 4. Inicializa o histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Eu sou seu Engenheiro SMT Assistente. Como posso ajudar a resolver as paradas de linha hoje?"}
    ]

# Renderiza as mensagens na tela
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. Caixa de texto para o Técnico digitar
if prompt := st.chat_input("Ex: O forno Heller está dando erro de temperatura na zona 3..."):
    # Salva e mostra a pergunta do técnico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Chama a IA do Google e mostra o "Carregando..."
    with st.chat_message("assistant"):
        with st.spinner("Analisando manuais SMT..."):
            try:
                # Transforma o histórico do Streamlit no formato do Google
                history = []
                for m in st.session_state.messages[:-1]:
                    if m["role"] == "assistant" and m == st.session_state.messages[0]: continue
                    role = "user" if m["role"] == "user" else "model"
                    history.append({"role": role, "parts": [m["content"]]})
                
                # Inicia a conversa e gera a resposta
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro de conexão com o Google: {e}")