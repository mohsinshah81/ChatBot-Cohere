import streamlit as st
import cohere

with st.sidebar:
  API_KEY = st.text_input("COHERE API KEY", key="chatbot_api_key", type="password")

st.title("Cohere Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "CHATBOT", "message": "Can I help?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["message"])

prompt = st.chat_input()

if prompt:
  if not API_KEY:
    st.info("Please enter Cohere API Key")
    st.stop()

    client = cohere.Client(API_KEY)
    st.chat_message("USER").write(prompt)

    response = client.chat(chat_history=st.session_state.messages, message=prompt)
    st.session_state.messages.append({"role": "USER", "message": prompt})
    msg = response.text

    st.session_state.messages.append({"role": "CHATBOT", "message": msg})
    st.chat_message("CHATBOT").write(msg)
