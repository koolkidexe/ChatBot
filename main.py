import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Load API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = model.generate_content(user_input)
    bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
