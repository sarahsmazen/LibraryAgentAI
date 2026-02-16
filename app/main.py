import streamlit as st
import requests
import uuid

# Backend endpoint
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Library Desk Agent", layout="wide")

# Sidebar for session management as requested in PDF 
st.sidebar.title("📚 Library Sessions")
if st.sidebar.button("➕ New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

# Main Interface 
st.title("🤖 Library AI Assistant")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt
if prompt := st.chat_input("Ask about books, orders, or stock..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = requests.post(f"{API_URL}/chat", json={
            "message": prompt, 
            "session_id": st.session_state.session_id
        })
        if response.status_code == 200:
            res_text = response.json().get("response")
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})