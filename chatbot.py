import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Rohit's Code Explainer",
    page_icon="💻",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f1117; }
    h1 { color: #00d4ff; text-align: center; }
    p { color: #888; text-align: center; }
    .stTextArea textarea { background-color: #1e1e2e; color: #cdd6f4; font-family: monospace; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>💻 Rohit's Code Explainer</h1>", unsafe_allow_html=True)
st.markdown("<p>Paste any code — AI will explain, debug and improve it</p>", unsafe_allow_html=True)
st.divider()

api_key = "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"
client = Groq(api_key=api_key)

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
