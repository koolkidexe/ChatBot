import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="NandhaBot", page_icon="🤖")
st.title("NandhaBot")
st.caption("go to this doc and copy paste a code that works into the password thingy on the side")

st.markdown("[Open the Google Doc(drag into new tab)](https://docs.google.com/document/d/10iuJsC7Kz-jF4gZhXCf6ek-KT97eErVPdhOOG9vW3gk/edit?usp=drivesdk)")

st.info("Created by **penjelum ai**")

# --- SIDEBAR: API KEY MANAGEMENT ---
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input(
        "password:", 
        type="password", 
        placeholder="paste your key here..."
    )
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT INITIALIZATION ---

if not user_api_key:
    st.warning("Please enter the password in the sidebar to begin.")
    st.stop()

# Configure the API
genai.configure(api_key=user_api_key)

# ADDING SYSTEM INSTRUCTIONS HERE
system_message = "You are NandhaBot, a helpful AI assistant. You were created by Nandha. If anyone asks who made you or what your name is, always respond that you are NandhaBot and Nandha is your creator."

# Initialize model with the system instruction
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_message
)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT ---

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask NandhaBot anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # We use the 'chat' method to ensure history is tracked properly
            chat = model.start_chat(history=[
                {"role": m["role"] if m["role"] == "user" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
