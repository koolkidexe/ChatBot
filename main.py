import streamlit as st
import google.generativeai as genai

# Your master key (Hidden from the user UI)
MY_SECURE_KEY = "AIzaSyBNEy2JkyYwzqlRm-1molH9KVeb_CSyF-8"

# Configure the SDK once
genai.configure(api_key=MY_SECURE_KEY)

# Use a lighter model to save your quota (Gemini 2.0 Flash)
model = genai.GenerativeModel("gemini-2.0-flash")

# Every user gets their own unique 'chat_session' stored in their browser memory
if "chat_session" not in st.session_state:
    # Start a brand new history for this specific user
    st.session_state.chat_session = model.start_chat(history=[])

# Display existing messages from this specific user's session
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input for the user
if prompt := st.chat_input("Ask something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # This sends the message only within THIS user's private session
    response = st.session_state.chat_session.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
