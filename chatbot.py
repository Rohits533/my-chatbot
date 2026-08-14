import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io

# 1. PAGE SETUP
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. INJECT CHAINGPT STYLE LIGHT TECHNICAL-GRID UI & ENTRY ANIMS
st.markdown("""
    <style>
    /* Entry Animations */
    @keyframes techFadeIn {
        0% { opacity: 0; transform: translateY(20px); filter: blur(2px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* ChainGPT Light Tech Theme Background */
    .stApp {
        background-color: #e6e8eb !important;
        background-image: 
            linear-gradient(to right, #d0d4dc 1px, transparent 1px),
            linear-gradient(to bottom, #d0d4dc 1px, transparent 1px) !important;
        background-size: 80px 80px !important;
        color: #0f1115 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Welcome Landing Wrapper */
    .welcome-container {
        text-align: center;
        margin-top: 15vh;
        animation: techFadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .welcome-subtitle {
        font-size: 14px;
        font-weight: 700;
        color: #ff5a1f;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .welcome-title {
        font-size: 72px;
        font-weight: 900;
        color: #0f1115;
        letter-spacing: -2px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    /* Updated Clean Top Header Ribbon Wrapper */
    .brand-top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 40px;
        background-color: #e6e8eb;
        border-bottom: 1px solid #c2c8d4;
        animation: techFadeIn 0.5s ease-out forwards;
    }
    .brand-logo-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-orange-cube {
        width: 14px;
        height: 14px;
        background-color: #ff5a1f;
    }
    .brand-logo-text {
        font-size: 16px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #0f1115;
        text-transform: uppercase;
    }
    .portfolio-link-button {
        display: inline-block;
        background-color: #0f1115;
        color: #ffffff !important;
        font-size: 11px;
        font-weight: 700;
        padding: 10px 22px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 4px;
        text-decoration: none !important;
        transition: background-color 0.2s ease;
    }
    .portfolio-link-button:hover {
        background-color: #242933;
    }

    /* Architectural Block Content Containers */
    .chaingpt-panel {
        background-color: #edf0f4 !important;
        border: 1px solid #b8bfc9 !important;
        padding: 35px !important;
        margin-bottom: 25px !important;
        position: relative;
        animation: techFadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .chaingpt-panel::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        width: 6px;
        height: 6px;
        background-color: #ff5a1f;
    }
    .chaingpt-panel::after {
        content: '';
        position: absolute;
        bottom: -3px;
        right: -3px;
        width: 6px;
        height: 6px;
        background-color: #ff5a1f;
    }

    /* Headings inside workspace panels */
    h1 {
        font-size: 40px !important;
        font-weight: 900 !important;
        color: #0f1115 !important;
        letter-spacing: -1px !important;
        text-transform: uppercase !important;
        margin: 0 0 10px 0 !important;
    }
    h3 {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ff5a1f !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin-bottom: 10px !important;
    }
    .panel-desc {
        font-size: 15px;
        color: #60687d;
        margin-bottom: 20px;
    }

    /* Universal Buttons */
    .stButton>button {
        background-color: #ff5a1f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 14px 32px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #e04a15 !important;
        transform: scale(1.02);
    }

    /* Input Controls Adjustment */
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        color: #0f1115 !important;
        border: 1px solid #b8bfc9 !important;
        border-radius: 4px !important;
    }

    /* Navigation Sidebar Adjustments */
    section[data-testid="stSidebar"] {
        background-color: #e1e4e9 !important;
        border-right: 1px solid #b8bfc9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INITIALIZE API BACKEND SYSTEMS
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# 4. INITIALIZE SESSION FLOW CONTROL KEYS
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

# 5. RENDER SYSTEM GATEWAY (LANDING PAGE)
if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-subtitle">SYSTEM INSTANCE INITIALIZATION</div>
            <div class="welcome-title">WELCOME TO<br>ROHIT'S CHATBOT</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        if st.button("ENTER CHATBOT SYSTEM 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()

# 6. UPDATED HEADER DEPLOYMENT (ONCE UNLOCKED)
st.markdown("""
    <div class="brand-top-nav">
        <div class="brand-logo-wrap">
            <div class="brand-orange-cube"></div>
            <div class="brand-logo-text">WELCOME TO ROHIT'S CHATBOT</div>
        </div>
        <a class="portfolio-link-button" href="https://github.io" target="_blank">🔗 VIEW MY PORTFOLIO</a>
    </div>
    <div style="margin-bottom: 30px;"></div>
""", unsafe_allow_html=True)

# 7. SIDEBAR SYSTEM NAVIGATION
st.sidebar.markdown("<h3 style='margin-top:10px;'>⚙️ CORE INSTANCES</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat",
    "🔍 Web Search Agent",
    "💻 Code Explainer",
    "📝 Quiz Generator",
    "📄 PDF Reader"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#60687d;'>POWERED BY LLAMA COMPILER ENGINE</div>", unsafe_allow_html=True)
# 8. RENDER CORE CHAT SERVICES
if page == "💬 Chat":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>BACKING THE VERY BEST BUILDERS</h3>
            <h1>💬 CORE CHAT SERVICES</h1>
            <div class="panel-desc">Transforming complex computing parameters into precise conversational study guides.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_space, col_reset = st.columns([5, 1])
    with col_reset:
        if st.button("🗑️ PURGE LOGS"):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask me anything or supply execution parameters...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("Processing Matrix Data Block..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        reply = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "🔍 Web Search Agent":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>REAL-TIME DISCOVERY NODES</h3>
            <h1>🔍 WEB SEARCH AGENT</h1>
            <div class="panel-desc">Scrapes external indexing arrays to return synchronized real-time web solutions.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    search_input = st.chat_input("Enter live network scrap search parameters...")
    if search_input:
        st.session_state.search_messages.append({"role": "user", "content": search_input})
        st.chat_message("user").write(search_input)
        with st.spinner("Running Network Queries..."):
            response = agent.invoke({"messages": [{"role": "user", "content": search_input}]})
            reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>RUNTIME LOGIC COMPILER</h3>
            <h1>💻 CODE DECONSTRUCTION</h1>
            <div class="panel-desc">Paste script elements to audit logic architecture, syntax bugs, or receive refactors.</div>
        </div>
    """, unsafe_allow_html=True)

    code_input = st.text_area("Source Code Array Buffer Input:", height=200, placeholder="def compute():\n    return 'Grid Verified'")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 DECONSTRUCT LOGIC")
    with col2:
        debug = st.button("🐛 IDENTIFY EXCEPTIONS")
    with col3:
        improve = st.button("⚡ ACCELERATE PERFORMANCE")

    if code_input:
        if explain:
            with st.spinner("Analyzing Stack..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>📖 LOGIC MAP BREAKDOWN</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if debug:
            with st.spinner("Compiling Array..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>🐛 SYNTAX EXCEPTIONS ENCOUNTERED</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if improve:
            with st.spinner("Refactoring Telemetry..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>⚡ PROPOSED SYSTEM OPTIMIZATIONS</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

elif page == "📝 Quiz Generator":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>COMPILING COMPREHENSION METRICS</h3>
            <h1>📝 ASSESSMENT NODE</h1>
            <div class="panel-desc">Convert raw topic arrays into tailored evaluation multiple choice training banks.</div>
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter Evaluation Focus Sub-Branch Topic:", placeholder="e.g. Backpropagation Math")
    num_questions = st.slider("Quantity of Target Examination Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE ASSESSMENT SCHEMATIC"):
        if topic:
            with st.spinner("Formulating Training Objects..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {num_questions} MCQ questions about {topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<h3>🎯 GENERATED TRAINING OBJECT FRAMEWORKS</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
        else:
            st.warning("Variable Declaration Missing: Enter a topic input first.")

elif page == "📄 PDF Reader":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>STRUCTURAL INDEX ANALYSIS</h3>
            <h1>📄 STRUCTURAL FILE PARSER</h1>
            <div class="panel-desc">Process heavy layout documentation blueprints to inspect underlying data context sheets.</div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Target System Document Package:", type="pdf")
    pdf_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page_num in pdf_reader.pages:
            pdf_text += page_num.extract_text()
        st.success("Target Content Dataset Synchronized Successfully.")

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    for msg in st.session_state.pdf_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    pdf_input = st.chat_input("Query structural document fields...")
    if pdf_input:
        st.session_state.pdf_messages.append({"role": "user", "content": pdf_input})
        st.chat_message("user").write(pdf_input)
        
        context_block = pdf_text if pdf_text else "No specific context dataset available."
        
        with st.spinner("Extracting Semantic Node Elements..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Answer the user's question accurately using only the provided document text context.\n\nContext:\n{context_block}"},
                    *st.session_state.pdf_messages
                ]
            )
        reply = response.choices.message.content
        st.session_state.pdf_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
