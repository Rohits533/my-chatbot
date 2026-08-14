import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io

# 1. EXPAND RUNTIME WEB WINDOW SCREEN SPACE
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INJECT INDUSTRIAL TECH MESH GRID SCHEMATIC AND CUSTOM CHAT STYLE ENGINE
st.markdown("""
    <style>
    /* Cascading System Entry Animations */
    @keyframes techFadeIn {
        0% { opacity: 0; transform: translateY(20px); filter: blur(4px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @keyframes matrixPulse {
        0% { box-shadow: 0 0 15px rgba(255, 90, 31, 0.15); border-color: #c2c8d4; }
        50% { box-shadow: 0 0 30px rgba(255, 90, 31, 0.4); border-color: #ff5a1f; }
        100% { box-shadow: 0 0 15px rgba(255, 90, 31, 0.15); border-color: #c2c8d4; }
    }
    @keyframes eyeGlow {
        0% { filter: drop-shadow(0 0 4px #00ffcc); }
        50% { filter: drop-shadow(0 0 12px #00ffcc); }
        100% { filter: drop-shadow(0 0 4px #00ffcc); }
    }

    /* Core Technical Blueprint Background Grid */
    .stApp {
        background-color: #e6e8eb !important;
        background-image: 
            linear-gradient(to right, #d0d4dc 1px, transparent 1px),
            linear-gradient(to bottom, #d0d4dc 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        color: #0f1115 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Entrance Dashboard Layout Formatter */
    .landing-hero {
        text-align: center;
        margin-top: 8vh;
        animation: techFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .landing-tagline {
        font-size: 13px;
        font-weight: 800;
        color: #ff5a1f;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    .landing-title {
        font-size: 86px;
        font-weight: 900;
        color: #0f1115;
        letter-spacing: -3px;
        text-transform: uppercase;
        line-height: 0.95;
        margin-bottom: 8px;
    }
    .landing-subtitle {
        font-size: 17px;
        font-weight: 600;
        color: #555e72;
        letter-spacing: 0.5px;
        margin-bottom: 45px;
    }

    /* Mechanical Robot Layout Framework */
    .mechanical-robot-canvas {
        width: 250px;
        height: 250px;
        background-color: #ffffff;
        border: 1px solid #c2c8d4;
        border-radius: 4px;
        margin: 0 auto 40px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        animation: matrixPulse 4s infinite ease-in-out;
    }
    .crosshair-tick {
        position: absolute; width: 6px; height: 6px; background-color: #ff5a1f;
    }
    .ct-tl { top: -3px; left: -3px; }
    .ct-tr { top: -3px; right: -3px; }
    .ct-bl { bottom: -3px; left: -3px; }
    .ct-br { bottom: -3px; right: -3px; }

    .robot-neck-mount {
        position: absolute; bottom: 25px; width: 90px; height: 40px;
        background-color: #e2e7ee; border: 1px solid #b8bfc9; border-radius: 4px;
    }
    .robot-head-shell {
        width: 150px; height: 150px; background-color: #ffffff;
        border: 1px solid #b8bfc9; border-radius: 44px; display: flex;
        justify-content: center; align-items: center; position: relative; z-index: 2;
    }
    .robot-neon-piping {
        position: absolute; top: 5px; left: 5px; right: 5px; bottom: 5px;
        border: 9px solid #ff5a1f; border-radius: 40px;
        box-shadow: 0 0 15px rgba(255, 90, 31, 0.4), inset 0 0 12px rgba(255, 90, 31, 0.3);
    }
    .robot-visor-display {
        width: 100px; height: 100px; background-color: #15171e;
        background-image: radial-gradient(rgba(255,255,255,0.06) 1px, transparent 0);
        background-size: 8px 8px; border-radius: 28px; display: flex;
        justify-content: center; align-items: center; gap: 18px; position: relative;
        z-index: 3; box-shadow: inset 0 4px 10px rgba(0,0,0,0.7);
    }
    .robot-matrix-optic {
        width: 12px; height: 12px; background-color: #00ffcc; border-radius: 50%;
        box-shadow: 0 0 10px #00ffcc, 0 0 18px rgba(0,255,204,0.6);
        animation: eyeGlow 3s infinite ease-in-out;
    }
    .ear-hinge-l { position: absolute; left: 39px; top: 107px; width: 12px; height: 35px; background-color: #ccd2db; border: 1px solid #b8bfc9; border-radius: 4px 0 0 4px; }
    .ear-hinge-r { position: absolute; right: 39px; top: 107px; width: 12px; height: 35px; background-color: #ccd2db; border: 1px solid #b8bfc9; border-radius: 0 4px 4px 0; }

    /* Top Horizontal Corporate Navigation Ribbon */
    .brand-top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        background-color: #e6e8eb;
        border-bottom: 1px solid #c2c8d4;
        animation: techFadeIn 0.5s ease-out forwards;
    }
    .brand-logo-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-orange-cube { width: 12px; height: 12px; background-color: #ff5a1f; }
    .brand-logo-text { font-size: 15px; font-weight: 900; letter-spacing: 1px; color: #0f1115; text-transform: uppercase; }
    
    .portfolio-link-button {
        display: inline-block; background-color: #0f1115; color: #ffffff !important;
        font-size: 11px; font-weight: 700; padding: 10px 22px; text-transform: uppercase;
        letter-spacing: 1px; border-radius: 4px; text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .portfolio-link-button:hover { background-color: #ff5a1f; box-shadow: 0 4px 15px rgba(255, 90, 31, 0.3); }

    /* Structural Panel Formats */
    .chaingpt-panel {
        background-color: #edf0f4 !important;
        border: 1px solid #b8bfc9 !important;
        border-radius: 4px !important;
        padding: 35px !important;
        margin-bottom: 25px !important;
        position: relative;
        animation: techFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .chaingpt-panel::before { content: ''; position: absolute; top: -3px; left: -3px; width: 6px; height: 6px; background-color: #ff5a1f; }
    .chaingpt-panel::after { content: ''; position: absolute; bottom: -3px; right: -3px; width: 6px; height: 6px; background-color: #ff5a1f; }

    /* Typography & Core Form Elements Overrides */
    h1 { font-size: 42px !important; font-weight: 900 !important; color: #0f1115 !important; letter-spacing: -1px !important; text-transform: uppercase !important; margin-top: 0px !important; }
    h3 { font-size: 13px !important; font-weight: 700 !important; color: #ff5a1f !important; text-transform: uppercase !important; letter-spacing: 2px !important; margin-bottom: 12px !important; }
    .panel-desc { font-size: 15px; color: #555e72; margin-bottom: 25px; }

    .stButton>button {
        background-color: #ff5a1f !important; color: #ffffff !important; border: none !important;
        border-radius: 4px !important; padding: 14px 32px !important; font-size: 12px !important;
        font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 1.5px !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 12px rgba(255, 90, 31, 0.2) !important;
    }
    .stButton>button:hover { background-color: #0f1115 !important; color: #ffffff !important; transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(15, 17, 21, 0.25) !important; }

    .stTextArea textarea, .stTextInput input { background-color: #ffffff !important; color: #0f1115 !important; border: 1px solid #b8bfc9 !important; border-radius: 4px !important; font-size: 14px !important; }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #ff5a1f !important; box-shadow: 0 0 0 1px #ff5a1f !important; }
    .stChatMessage { background-color: #ffffff !important; border: 1px solid #dcdfe6 !important; border-radius: 8px !important; padding: 16px !important; margin-bottom: 12px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important; }
    section[data-testid="stSidebar"] { background-color: #e1e4e9 !important; border-right: 1px solid #b8bfc9 !important; }
    </style>
""", unsafe_allow_html=True)
# 3. INITIALIZE SECURE ENDPOINT MODELS OVER CONNECTIONS
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# 4. APP GATEWAY FLOW VALIDATORS
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

# Gateway Display Rendering Module
if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="landing-hero">
            <div class="landing-tagline">BACKING TOMORROW // ROBIT CORE ENGINE</div>
            <div class="landing-title">KUBOOM CHATBOT</div>
            <div class="landing-subtitle">A chatbot made by Rohit</div>
            
            <div class="mechanical-robot-canvas">
                <div class="crosshair-tick ct-tl"></div><div class="crosshair-tick ct-tr"></div>
                <div class="crosshair-tick ct-bl"></div><div class="crosshair-tick ct-br"></div>
                <div class="robot-neck-mount"></div>
                <div class="robot-head-shell">
                    <div class="robot-neon-piping"></div>
                    <div class="robot-visor-display">
                        <div class="robot-matrix-optic"></div><div class="robot-matrix-optic"></div>
                    </div>
                </div>
                <div class="ear-hinge-l"></div><div class="ear-hinge-r"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l, col_btn, col_r = st.columns([1, 1.2, 1])
    with col_btn:
        if st.button("LAUNCH WORKSPACE MODULE 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()

# 5. GLOBAL HORIZONTAL BRAND COMPONENT DEPLOYMENT
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

# Sidebar System Instance Menu
st.sidebar.markdown("<h3 style='margin-top:10px;'>⚙️ UTILITY NODES</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat Engine",
    "🔍 Web Search Node",
    "💻 Code Explainer",
    "📝 Quiz Matrix",
    "📄 PDF Structural Parser"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#60687d;'>DESIGN COMPILED BY ROHIT • METAMATRIX ENGINE</div>", unsafe_allow_html=True)
# ==========================================
# 6. APPLICATION ROUTINE INSTANCE SWITCHES
# ==========================================

# A. LIVE CONVERSATIONAL CORE MODULE
if page == "💬 Chat Engine":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>CORE CONVERSATIONAL MATRIX</h3>
            <h1>💬 CORE CHAT SERVICES</h1>
            <div class="panel-desc">Direct interface to processing model blocks for computer science, curriculum engineering, and coding tutorials.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_space, col_reset = st.columns()  # Configuration lengths passed to protect column alignments
    with col_reset:
        if st.button("🗑️ PURGE STORAGE", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Enter conversational string payload blocks...")
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

# B. AUTONOMOUS NETWORK SCRAPER SEARCH ENGINE
elif page == "🔍 Web Search Node":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>REALTIME DISCOVERY ARRAYS</h3>
            <h1>🔍 WEB SEARCH MODULE</h1>
            <div class="panel-desc">Runs automated queries against network endpoints to return up-to-date documentation schemas.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    search_input = st.chat_input("Enter target live exploration parameters...")
    if search_input:
        st.session_state.search_messages.append({"role": "user", "content": search_input})
        st.chat_message("user").write(search_input)
        with st.spinner("Invoking Autonomous Data Extraction Node..."):
            response = agent.invoke({"messages": [{"role": "user", "content": search_input}]})
            reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
# C. RUNTIME SCRIPT ANALYSIS COMPILER ENGINE
elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>RUNTIME LOGIC INTERCEPT</h3>
            <h1>💻 CODE DECONSTRUCTION</h1>
            <div class="panel-desc">Paste script components to map out logic structures, handle syntax bugs, and calculate optimizations.</div>
        </div>
    """, unsafe_allow_html=True)

    code_input = st.text_area("Source Code Array Buffer Input:", height=200, placeholder="def runtime_matrix():\n    return 'Execution Verified'")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 EXPLAIN SCRIPT ARCHITECTURE", use_container_width=True)
    with col2:
        debug = st.button("🐛 DIAGNOSE EXCEPTIONS", use_container_width=True)
    with col3:
        improve = st.button("⚡ ACCELERATE PERFORMANCE", use_container_width=True)

    if code_input:
        if explain:
            with st.spinner("Tracing Call Trees..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="chaingpt-panel"><h3>📖 STRUCTURAL BREAKDOWN</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if debug:
            with st.spinner("Scanning Exceptions..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="chaingpt-panel"><h3>🐛 SYNTAX EXCEPTIONS ENCOUNTERED</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if improve:
            with st.spinner("Calculating Performance O-Complexities..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="chaingpt-panel"><h3>⚡ REFACTORED WORKSPACE BLOCKS</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)

# D. TOPIC COMPREHENSION EXAMINATION MATRIX GENERATOR
elif page == "📝 Quiz Matrix":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>COMPILING COMPREHENSION OBJECTS</h3>
            <h1>📝 MCQ EVALUATION GENERATOR</h1>
            <div class="panel-desc">Convert instruction variables into tailored multiple-choice training sets.</div>
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter Focus Subject Topic Node:", placeholder="e.g. Backpropagation Matrices")
    num_questions = st.slider("Quantity of Target Examination Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE ASSESSMENT BLOCKS", use_container_width=True):
        if topic:
            with st.spinner("Formulating Training Objects..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {num_questions} MCQ questions about {topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<div class="chaingpt-panel"><h3>🎯 TARGET GENERATED EVALUATION MODELS</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Variable Declaration Missing: Supply topic parameter input first.")

# E. STRUCTURAL FILE PARSING RECONSTRUCTION MODULE
elif page == "📄 PDF Structural Parser":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>INDEX CONTENT INTERROGATOR</h3>
            <h1>📄 STRUCTURAL FILE PARSER</h1>
            <div class="panel-desc">Process heavy layout documentation blueprints to inspect underlying static contexts.</div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Target System Document Package:", type="pdf")
    pdf_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page_num in pdf_reader.pages:
            pdf_text += page_num.extract_text()
        st.success("Target Content Dataset Mounted Successfully.")

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
