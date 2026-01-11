import streamlit as st
import cohere

# Sidebar for API key
with st.sidebar:
    API_KEY = st.text_input(
        "COHERE API KEY",
        type="password"
    )

st.title("Cohere Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Can I help?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    if not API_KEY:
        st.info("Please enter Cohere API Key")
        st.stop()

    # Initialize Cohere client
    client = cohere.Client(API_KEY)

    # Display user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Convert history for Cohere
    cohere_history = [
        {
            "role": "USER" if m["role"] == "user" else "CHATBOT",
            "message": m["content"]
        }
        for m in st.session_state.messages[:-1]
    ]

    # Call Cohere
    response = client.chat(
        message=prompt,
        chat_history=cohere_history
    )

    # Display assistant response
    msg = response.text
    st.chat_message("assistant").write(msg)
    st.session_state.messages.append(
        {"role": "assistant", "content": msg}
    )
