import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="penjelum ai")
st.title("NandhaBot")
st.caption("u gotta copy paste this into the password thingy to get it to work: AIzaSyBBQh6vsTvZTS2ptHN28EjVVxsOS_Vcf1Y")

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

# Check if the user has provided a key
if not user_api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
    st.stop()

# Configure the API with the user's provided key
genai.configure(api_key=user_api_key)
model = genai.GenerativeModel("gemini-2.0")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT ---

# Show history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What's up?"):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using the provided key
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # We use stream=True for that modern "typing" feel
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            # Save the final response
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Handle invalid keys or API errors gracefully
            st.error(f"Error: {e}")
            if "API_KEY_INVALID" in str(e):
                st.info("Your API key seems incorrect. Please check it in the sidebar.")
