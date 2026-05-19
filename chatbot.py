import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f1117; }
    .stChatMessage { border-radius: 12px; padding: 10px; }
    .stTextInput input { border-radius: 20px; }
    h1 { color: #00d4ff; text-align: center; }
    p { color: #888; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 Rohit's AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p>Powered by Llama 3 • Built by Rohit</p>", unsafe_allow_html=True)
st.divider()

api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are Rohit's personal AI Study & Coding Assistant. 
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
When someone shares code, you analyze it and suggest improvements.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""
        }
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
