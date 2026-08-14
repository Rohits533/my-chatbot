import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. INJECT CHAINGPT EXPERIMENTAL LIGHT GRID DESIGN SYSTEM
st.markdown("""
    <style>
    /* Premium Entry Animations */
    @keyframes techFadeIn {
        0% { opacity: 0; transform: translateY(25px); filter: blur(4px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* Core Technical Blueprint Background Grid */
    .stApp {
        background-color: #e6e8eb !important;
        background-image: 
            linear-gradient(to right, #d0d4dc 1px, transparent 1px),
            linear-gradient(to bottom, #d0d4dc 1px, transparent 1px) !important;
        background-size: 80px 80px !important;
        color: #0f1115 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Entry Dashboard Container alignment */
    .landing-hero {
        text-align: center;
        margin-top: 5vh;
        animation: techFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .landing-tagline {
        font-size: 13px;
        font-weight: 800;
        color: #ff5a1f;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .landing-title {
        font-size: 84px;
        font-weight: 900;
        color: #0f1115;
        letter-spacing: -3px;
        text-transform: uppercase;
        line-height: 0.95;
        margin-bottom: 5px;
    }
    .landing-subtitle {
        font-size: 16px;
        font-weight: 600;
        color: #60687d;
        letter-spacing: 0.5px;
        margin-bottom: 35px;
    }

    /* Top Workspace Header Navigation Strip */
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
    .brand-orange-cube {
        width: 12px;
        height: 12px;
        background-color: #ff5a1f;
    }
    .brand-logo-text {
        font-size: 15px;
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
    }
    .portfolio-link-button:hover {
        background-color: #242933;
    }

    /* Technical Content Workspace Blocks */
    .chaingpt-panel {
        background-color: #edf0f4 !important;
        border: 1px solid #b8bfc9 !important;
        padding: 35px !important;
        margin-bottom: 25px !important;
        position: relative;
        animation: techFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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

    /* Global UI Form Controls and Elements */
    h1 {
        font-size: 38px !important;
        font-weight: 900 !important;
        color: #0f1115 !important;
        text-transform: uppercase !important;
        margin-top: 0px !important;
    }
    h3 {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ff5a1f !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    .panel-desc {
        font-size: 15px;
        color: #60687d;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #ff5a1f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 14px 32px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    .stButton>button:hover {
        background-color: #e04a15 !important;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        color: #0f1115 !important;
        border: 1px solid #b8bfc9 !important;
        border-radius: 4px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #e1e4e9 !important;
        border-right: 1px solid #b8bfc9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INITIALIZE BACKEND API CONNECTIONS
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# 4. FLOW APP GATEWAY STATE CHECK
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

# 5. ENTRY SYSTEM DASHBOARD OVERLAY WITH THE UPGRADED DESIGNER ROBOT VISOR
if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="landing-hero">
            <div class="landing-tagline">BACKING TOMORROW // ROBIT CORE</div>
            <div class="landing-title">KUBOOM CHATBOT</div>
            <div class="landing-subtitle">A chatbot made by Rohit</div>
            
            <!-- Upgraded Designer Robot Vector Canvas Graphic -->
            <div style="
                width: 260px;
                height: 260px;
                background-color: #ffffff;
                border: 1px solid #b8bfc9;
                border-radius: 8px;
                margin: 0 auto 40px auto;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            ">
                <div style="
                    position: absolute;
                    bottom: 0;
                    width: 120px;
                    height: 35px;
                    background-color: #ccd2db;
                    border: 1px solid #b8bfc9;
                    border-radius: 4px 4px 0 0;
                "></div>
                <div style="
                    width: 170px;
                    height: 170px;
                    background-color: #ffffff;
                    border: 1px solid #b8bfc9;
                    border-radius: 40px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    position: relative;
                    z-index: 2;
                ">
                    <div style="
                        position: absolute;
                        top: 6px;
                        left: 6px;
                        right: 6px;
                        bottom: 6px;
                        border: 10px solid #ff5a1f;
                        border-radius: 34px;
                        box-shadow: 0 0 20px rgba(255, 90, 31, 0.6), inset 0 0 15px rgba(255, 90, 31, 0.4);
                    "></div>
                    <div style="
                        width: 110px;
                        height: 110px;
                        background-color: #1a1d24;
                        background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 0);
                        background-size: 8px 8px;
                        border-radius: 24px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 22px;
                        position: relative;
                        z-index: 3;
                        box-shadow: inset 0 4px 10px rgba(0,0,0,0.8);
                    ">
                        <div style="width: 14px; height: 14px; background-color: #ffffff; border-radius: 50%; box-shadow: 0 0 14px #ffffff, 0 0 25px rgba(255,255,255,0.8);"></div>
                        <div style="width: 14px; height: 14px; background-color: #ffffff; border-radius: 50%; box-shadow: 0 0 14px #ffffff, 0 0 25px rgba(255,255,255,0.8);"></div>
                    </div>
                </div>
                <div style="position: absolute; left: 33px; top: 115px; width: 16px; height: 32px; background-color: #b8bfc9; border-radius: 4px 0 0 4px;"></div>
                <div style="position: absolute; right: 33px; top: 115px; width: 16px; height: 32px; background-color: #b8bfc9; border-radius: 0 4px 4px 0;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l, col_btn, col_r = st.columns([1, 1.2, 1])
    with col_btn:
        if st.button("LAUNCH WORKSPACE MODULE 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()
# 6. APPLICATION SYSTEM NAVIGATION BANNER
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

# 7. SIDEBAR FRAME SELECTION
st.sidebar.markdown("<h3 style='margin-top:10px;'>⚙️ UTILITY NODES</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat",
    "🔍 Web Search Agent",
    "💻 Code Explainer",
    "📝 Quiz Generator",
    "📄 PDF Reader"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#60687d;'>COMPILED BY ROHIT • METAMATRIX ENGINE</div>", unsafe_allow_html=True)

# 8. WORKSPACE CONTROL ROUTINES
if page == "💬 Chat":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>CORE SYSTEM DATASTREAM</h3>
            <h1>💬 CONVERSATIONAL ASSISTANT</h1>
            <div class="panel-desc">Direct interface to standard processing matrix blocks for computer science, engineering, and coding updates.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_space, col_reset = st.columns([4, 1])  # Explicit sizing configurations passed to avoid layout leaks
    with col_reset:
        if st.button("🗑️ PURGE BUFFER LOGS"):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Enter message packet parameters...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("Processing Token Arrays..."):
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
            <h3>REALTIME SCRAPING ARRAYS</h3>
            <h1>🔍 WEB SEARCH NODE</h1>
            <div class="panel-desc">Queries live network records to cross-reference system queries against active global domains.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    search_input = st.chat_input("Input network crawler search strings...")
    if search_input:
        st.session_state.search_messages.append({"role": "user", "content": search_input})
        st.chat_message("user").write(search_input)
        with st.spinner("Invoking Crawl Matrix..."):
            response = agent.invoke({"messages": [{"role": "user", "content": search_input}]})
            reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>SYNTAX REFACTOR RUNTIME</h3>
            <h1>💻 CODE DECONSTRUCTION</h1>
            <div class="panel-desc">Paste engineering scripts to trace call stacks, audit runtime bugs, and optimize logic fields.</div>
        </div>
    """, unsafe_allow_html=True)

    code_input = st.text_area("Source Code Array Input Buffer:", height=200, placeholder="def active_matrix():\n    return 'Telemetry Stable'")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 EXPLAIN PATTERNS")
    with col2:
        debug = st.button("🐛 AUDIT SYNTAX")
    with col3:
        improve = st.button("⚡ ACCELERATE RUNTIME")

    if code_input:
        if explain:
            with st.spinner("Mapping Call Trees..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>📖 ARCHITECTURAL EXPLANATION</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if debug:
            with st.spinner("Scanning Assembly Exceptions..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>🐛 RUNTIME CONTEXT EXCEPTIONS IDENTIFIED</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if improve:
            with st.spinner("Optimizing Memory Allocations..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>⚡ REFACTORED COMPUTATIONAL OUTLINES</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

elif page == "📝 Quiz Generator":
    st.markdown("""
        <div class="chaingpt-panel">
            <h3>COMPILING SYSTEM TESTS</h3>
            <h1>📝 MCQ EVALUATION GENERATOR</h1>
            <div class="panel-desc">Generate detailed, customized multiple choice practice templates dynamically from instructional string targets.</div>
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter Evaluation Focus Sub-Branch Topic:", placeholder="e.g. Backpropagation Math")
    num_questions = st.slider("Quantity of Target Examination Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE EXAMINATION SCHEMATICS"):
        if topic:
            with st.spinner("Compiling Training Set Objects..."):
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

    pdf_input = st.chat_input("Query file data structures here...")
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
