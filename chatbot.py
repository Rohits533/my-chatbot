import streamlit as st
from groq import Groq
import PyPDF2
import io

st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f1117; }
    .stChatMessage { border-radius: 12px; padding: 10px; }
    h1 { color: #00d4ff; text-align: center; }
    p { color: #888; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 Rohit's AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p>Powered by Llama 3 • Built by Rohit</p>", unsafe_allow_html=True)
st.divider()

api_key = "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"
client = Groq(api_key=api_key)

uploaded_file = st.file_uploader("📄 Upload a PDF to chat with it", type="pdf")

pdf_text = ""
if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    st.success("✅ PDF loaded! Ask me anything about it.")

system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

if pdf_text:
    system_prompt += f"\n\nThe user has uploaded a document. Use this to answer their questions:\n{pdf_text[:6000]}"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
