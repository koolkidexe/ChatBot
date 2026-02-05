import streamlit as st
import google.generativeai as genai
import os

# 🔑 Put your API key here (or use env variables)
genai.configure(api_key="AIzaSyAG-6gxQbbYDjaKXbCjdl9doJvDHIrPCyo")

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    response = st.session_state.chat.send_message(user_input)
    st.write("**Gemini:**", response.text)
