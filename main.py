import streamlit as st
import google.generativeai as genai
import os, json, uuid
from dotenv import load_dotenv

# ---------- SETUP ----------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"
MEMORY_DIR = "memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

model = genai.GenerativeModel(MODEL_NAME)

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# ---------- USER ID ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

user_id = st.session_state.user_id
memory_file = f"{MEMORY_DIR}/{user_id}.json"

# ---------- LOAD MEMORY ----------
def load_history():
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(memory_file, "w") as f:
        json.dump(history, f)

history = load_history()

# ---------- CHAT ----------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=history)

# ---------- UI ----------
for msg in st.session_state.chat.history:
    role = "🧑 You" if msg["role"] == "user" else "🤖 Gemini"
    st.markdown(f"**{role}:** {msg['parts'][0]}")

prompt = st.text_input("Message")

if st.button("Send") and prompt:
    response = st.session_state.chat.send_message(prompt)
    save_history(st.session_state.chat.history)
    st.experimental_rerun()

# ---------- CLEAR MEMORY ----------
if st.button("Clear Memory"):
    st.session_state.chat = model.start_chat(history=[])
    save_history([])
    st.experimental_rerun()
