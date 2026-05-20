import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

st.set_page_config(
    page_title="Rohit's AI Agent",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f1117; }
    h1 { color: #00d4ff; text-align: center; }
    p { color: #888; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🔍 Rohit's AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<p>Powered by LangChain + DuckDuckGo • Knows today's news</p>", unsafe_allow_html=True)
st.divider()

api_key = "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"

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)

search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask me anything — I can search the web!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Searching the web..."):
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        reply = response["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
