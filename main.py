import streamlit as st
import google.generativeai as genai

# === Page Config ===
st.set_page_config(page_title="NandhaBot - Chatbot", layout="centered")

# === Custom CSS for styling ===
st.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
    }
    .stApp {
        background: linear-gradient(to bottom right, #dbeafe, #fef9c3);
        padding: 2rem;
    }
    .title {
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 1rem;
        color: #1e3a8a;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-left: 6px solid;
    }
    .chat-message.user {
        background-color: #ecfdf5;
        border-color: #10b981;
    }
    .chat-message.assistant {
        background-color: #eef2ff;
        border-color: #6366f1;
    }
    </style>
""", unsafe_allow_html=True)

# === Title ===
st.markdown('<div class="title">NandhaBot</div>', unsafe_allow_html=True)
st.markdown("Ask anything — NandhaBot: AI Virtual Assistant.")

# === Sidebar ===
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password", key="api_key")
view_history = st.sidebar.checkbox("Show history")

# === Require API Key ===
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")
    st.stop()

# === Configure Gemini ===
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# === Init session states ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = {}

# === Load and resume past chat ===
if view_history:
    st.subheader("Past Conversations")

    user_history = st.session_state.history.get(api_key, [])
    if not user_history:
        st.info("No past conversations found for this API key.")
        st.stop()

    titles = [entry["title"] for entry in user_history]
    selection = st.selectbox("Select a conversation to resume", titles)
    index = titles.index(selection)
    convo = user_history[index]["messages"]

    if st.button("Load Conversation"):
        st.session_state.messages = convo.copy()
        st.success("Conversation loaded. You can continue chatting below.")

# === Display chat messages ===
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f'<div class="chat-message {role_class}"><strong>{msg["role"].capitalize()}</strong>: {msg["content"]}</div>',
        unsafe_allow_html=True
    )

# === Chat Input ===
user_input = st.chat_input("Say something to NandhaBot...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(
        f'<div class="chat-message user"><strong>User</strong>: {user_input}</div>',
        unsafe_allow_html=True
    )

    # Build chat context
    chat_history = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "NandhaBot"
        chat_history += f"{role}: {msg['content']}\n"
    chat_history += "NandhaBot:"

    # Get Gemini response
    try:
        response = model.generate_content(chat_history)
        reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown(
            f'<div class="chat-message assistant"><strong>NandhaBot</strong>: {reply}</div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        error_msg = f"Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.markdown(
            f'<div class="chat-message assistant"><strong>NandhaBot</strong>: {error_msg}</div>',
            unsafe_allow_html=True
        )

# === Save Conversation ===
def save_conversation():
    if st.session_state.messages:
        if api_key not in st.session_state.history:
            st.session_state.history[api_key] = []

        # Use first user message or fallback title
        title = "Untitled Conversation"
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                title = msg["content"][:40].strip() + "..." if len(msg["content"]) > 40 else msg["content"]
                break

        # Save conversation with title
        st.session_state.history[api_key].append({
            "title": title,
            "messages": st.session_state.messages.copy()
        })

        st.session_state.messages = []

st.button("End Chat and Save", on_click=save_conversation)
