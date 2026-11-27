import streamlit as st

from abrobalocal import NOME, apresentacao, responder

st.set_page_config(page_title=NOME)
st.title(NOME)

if "conversa" not in st.session_state:
    boas_vindas = apresentacao().replace(" ou 'sair' para encerrar", "")
    st.session_state.conversa = [("assistant", boas_vindas)]

mensagem = st.chat_input("Digite sua pergunta")
if mensagem:
    st.session_state.conversa.append(("user", mensagem))
    st.session_state.conversa.append(("assistant", responder(mensagem)))

for quem, texto in st.session_state.conversa:
    with st.chat_message(quem):
        st.text(texto)
