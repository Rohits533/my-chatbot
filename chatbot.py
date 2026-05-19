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
    h3 { color: #00d4ff; }
    p { color: #888; text-align: center; }
    .stTextArea textarea { background-color: #1e1e2e; color: #cdd6f4; font-family: monospace; border-radius: 10px; }
    .stSidebar { background-color: #1e1e2e; }
    </style>
""", unsafe_allow_html=True)

api_key = "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"
client = Groq(api_key=api_key)

st.sidebar.markdown("# 🤖 Rohit's AI Assistant")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["💬 Chat", "💻 Code Explainer", "📝 Quiz Generator"])
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Rohit** • Powered by Llama 3")

if page == "💬 Chat":
    st.markdown("<h1>💬 AI Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p>Your personal Study & Coding Assistant</p>", unsafe_allow_html=True)
    st.divider()

    uploaded_file = st.file_uploader("📄 Upload a PDF to chat with it", type="pdf")
    pdf_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page_num in pdf_reader.pages:
            pdf_text += page_num.extract_text()
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

elif page == "💻 Code Explainer":
    st.markdown("<h1>💻 Code Explainer</h1>", unsafe_allow_html=True)
    st.markdown("<p>Paste any code — AI will explain, debug and improve it</p>", unsafe_allow_html=True)
    st.divider()

    code_input = st.text_area("Paste your code here:", height=250, placeholder="def hello():\n    print('Hello World')")
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 Explain")
    with col2:
        debug = st.button("🐛 Find Bugs")
    with col3:
        improve = st.button("⚡ Improve")

    if code_input:
        if explain:
            with st.spinner("Analyzing..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown("### 📖 Explanation")
            st.write(response.choices[0].message.content)

        if debug:
            with st.spinner("Finding bugs..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown("### 🐛 Bugs Found")
            st.write(response.choices[0].message.content)

        if improve:
            with st.spinner("Improving..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown("### ⚡ Improvements")
            st.write(response.choices[0].message.content)
    else:
        st.info("👆 Paste some code above to get started!")

elif page == "📝 Quiz Generator":
    st.markdown("<h1>📝 Quiz Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p>Enter any topic — AI generates MCQ questions for exam prep</p>", unsafe_allow_html=True)
    st.divider()

    topic = st.text_input("Enter a topic:", placeholder="e.g. Python loops, Machine Learning, Data Structures")
    num_questions = st.slider("Number of questions:", 3, 10, 5)

    if st.button("🎯 Generate Quiz"):
        if topic:
            with st.spinner("Generating quiz..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {num_questions} MCQ questions about {topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown("### 🎯 Your Quiz")
            st.write(response.choices[0].message.content)
        else:
            st.warning("Please enter a topic first!")
