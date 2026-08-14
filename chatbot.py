import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io
import time

# =============================================================================
# 1. CORE STREAMLIT INSTANCE INIT & LAYOUT SYSTEM
# =============================================================================
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. INJECT ADVANCED ACCELERATED KEYFRAME CSS ROUTINES
# =============================================================================
st.markdown("""
    <style>
    /* Cinematic Telemetry Entry Hardware Animations */
    @keyframes entryZoomFade {
        0% { opacity: 0; transform: scale(0.96) translateY(40px); filter: blur(10px); }
        40% { opacity: 0.5; filter: blur(4px); }
        100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
    }
    @keyframes fluidPanelSlide {
        0% { opacity: 0; transform: translateY(25px); filter: blur(4px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @keyframes pulseTargetCrosshair {
        0% { box-shadow: 0 0 10px rgba(255, 90, 31, 0.2); border-color: #0f1115; }
        50% { box-shadow: 0 0 25px rgba(255, 90, 31, 0.6); border-color: #ff5a1f; }
        100% { box-shadow: 0 0 10px rgba(255, 90, 31, 0.2); border-color: #0f1115; }
    }
    @keyframes gridMeshScroll {
        0% { background-position: 0px 0px; }
        100% { background-position: 60px 60px; }
    }

    /* Core Architectural Blueprint Mesh Layout Background Configuration */
    .stApp {
        background-color: #e6e8eb !important;
        background-image: 
            linear-gradient(to right, #ccd2db 1px, transparent 1px),
            linear-gradient(to bottom, #ccd2db 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        color: #0f1115 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif !important;
        animation: gridMeshScroll 30s linear infinite;
    }

    /* Gateway Landing Dashboard Hero Wrapper */
    .gateway-entry-container {
        text-align: center;
        margin-top: 12vh;
        padding: 50px;
        background-color: rgba(230, 232, 235, 0.7);
        border: 2px dashed #b8bfc9;
        border-radius: 8px;
        backdrop-filter: blur(10px);
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        animation: entryZoomFade 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .gateway-tagline {
        font-size: 13px;
        font-weight: 800;
        color: #ff5a1f;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 25px;
    }
    .gateway-title {
        font-size: 88px;
        font-weight: 900;
        color: #0f1115;
        letter-spacing: -3px;
        text-transform: uppercase;
        line-height: 0.95;
        margin-bottom: 15px;
    }
    .gateway-subtitle {
        font-size: 19px;
        font-weight: 600;
        color: #555e72;
        letter-spacing: 0.5px;
        margin-bottom: 50px;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Top Horizontal Corporate Navigation Component Bar Banner */
    .brand-navigation-ribbon {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 45px;
        background-color: #e6e8eb;
        border-bottom: 2px solid #b8bfc9;
        margin-bottom: 0px;
        animation: fluidPanelSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .brand-logo-cluster {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-orange-block {
        width: 14px;
        height: 14px;
        background-color: #ff5a1f;
    }
    .brand-logo-text-string {
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #0f1115;
        text-transform: uppercase;
    }
    
    /* Neo-Brutalist Technical Panel Workspace Shell Modules */
    .neobrutalist-content-card {
        background-color: #edf0f4 !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 45px !important;
        margin-bottom: 35px !important;
        position: relative;
        box-shadow: 6px 6px 0px #0f1115 !important;
        animation: fluidPanelSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Technical Blueprint Mesh Corner ticks */
    .neobrutalist-content-card::before {
        content: '';
        position: absolute;
        top: -6px;
        left: -6px;
        width: 10px;
        height: 10px;
        background-color: #ff5a1f;
        border: 2px solid #0f1115;
    }
    .neobrutalist-content-card::after {
        content: '';
        position: absolute;
        bottom: -6px;
        right: -6px;
        width: 10px;
        height: 10px;
        background-color: #ff5a1f;
        border: 2px solid #0f1115;
    }

    /* Core Native Elements Typographical Configurations Overrides */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 46px !important;
        font-weight: 900 !important;
        color: #0f1115 !important;
        letter-spacing: -1px !important;
        text-transform: uppercase !important;
        margin-top: 0px !important;
        margin-bottom: 12px !important;
    }
    h2 { font-size: 24px !important; font-weight: 800 !important; color: #0f1115 !important; text-transform: uppercase !important; }
    h3 { font-size: 13px !important; font-weight: 800 !important; color: #ff5a1f !important; text-transform: uppercase !important; letter-spacing: 3px !important; margin-bottom: 10px !important; }
    .card-narrative-paragraph { font-size: 15.5px; line-height: 1.6; color: #555e72; margin-bottom: 25px; }

    /* Premium Block Core Buttons Customization Layout */
    .stButton>button {
        background-color: #ff5a1f !important;
        color: #ffffff !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 15px 35px !important;
        font-size: 12.5px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        box-shadow: 4px 4px 0px #0f1115 !important;
        transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton>button:hover {
        background-color: #0f1115 !important;
        color: #ffffff !important;
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px #0f1115 !important;
    }
    .stButton>button:active {
        transform: translate(4px, 4px) !important;
        box-shadow: 0px 0px 0px #0f1115 !important;
    }

    /* Functional Processing Form Elements Styling Customization */
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        color: #0f1115 !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        font-family: monospace !important;
        padding: 14px !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ff5a1f !important;
        box-shadow: none !important;
    }

    /* High-End Dark Workspace Chat Logs Layout */
    .stChatMessage {
        background-color: #171923 !important;
        color: #ffffff !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 22px !important;
        margin-bottom: 15px !important;
        box-shadow: 4px 4px 0px #0f1115 !important;
        animation: fluidPanelSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Left Sidebar Global Panel Formats Intercept */
    section[data-testid="stSidebar"] {
        background-color: #d8dbe2 !important;
        border-right: 3px solid #0f1115 !important;
    }
    </style>
""", unsafe_allow_html=True)
# =============================================================================
# 3. SECURE REPOSITORY BACKEND CLIENT INTEGRATIONS
# =============================================================================
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# =============================================================================
# 4. APP SYSTEM RUNTIME ACCESS STATE GATEWAY
# =============================================================================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

# Render Gateway Landing Overlay Shell
if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="gateway-entry-container">
            <div class="gateway-tagline">INITIALIZING CORE ACCESS PARSING SYSTEM</div>
            <div class="gateway-title">KUBOOM CHATBOT</div>
            <div class="gateway-subtitle">A chatbot made by Rohit</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_entry_l, col_entry_btn, col_entry_r = st.columns([1, 1.4, 1])
    with col_entry_btn:
        if st.button("LAUNCH WORKSPACE ENGINES 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()

# =============================================================================
# 5. GLOBAL HORIZONTAL BRAND SYSTEM RIBBON NAVIGATION MOCK
# =============================================================================
st.markdown("""
    <div class="brand-navigation-ribbon">
        <div class="brand-logo-cluster">
            <div class="brand-orange-block"></div>
            <div class="brand-logo-text-string">WELCOME TO ROHIT'S CHATBOT</div>
        </div>
        <a style="
            display: inline-block;
            background-color: #0f1115;
            color: #ffffff !important;
            font-size: 11px;
            font-weight: 800;
            padding: 12px 24px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border: 2px solid #0f1115;
            border-radius: 0px;
            text-decoration: none !important;
            box-shadow: 4px 4px 0px #ff5a1f;
            transition: all 0.2s ease;
        " href="https://github.io" target="_blank">🔗 VIEW PORTFOLIO</a>
    </div>
    <div style="margin-bottom: 40px;"></div>
""", unsafe_allow_html=True)

# Left Sidebar Instance Selectors
st.sidebar.markdown("<h3 style='margin-top:10px;'>⚙️ UTILITY FRAMEWORK</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat Matrix",
    "🔍 Realtime Web Crawler",
    "💻 Code Explainer",
    "📝 Examination Quiz",
    "📄 Document Structural Parser"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#555e72; font-weight:800; text-transform:uppercase;'>COMPILED BY ROHIT • METAMATRIX ENGINE</div>", unsafe_allow_html=True)
# =============================================================================
# 6. INSTANCE CONTROL SWITCH PROCESSING LOGIC
# =============================================================================

# A. CORE CHAT ENGINE MODULE
if page == "💬 Chat Matrix":
    st.markdown("""
        <div class="neobrutalist-content-card">
            <h3>CORE CONVERSATIONAL MATRIX</h3>
            <h1>💬 CONVERSATIONAL ASSISTANT</h1>
            <div class="card-narrative-paragraph">Direct interface to processing model layers for engineering, technology, curriculum structures, and coding modules.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_empty_spacer, col_clear_trigger = st.columns([3.6, 1.4])
    with col_clear_trigger:
        if st.button("🗑️ PURGE MEMORY LOGS", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    # Active message loop output formatting
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    chat_matrix_input = st.chat_input("Enter system conversational string payload parameters...")
    if chat_matrix_input:
        st.session_state.messages.append({"role": "user", "content": chat_matrix_input})
        st.chat_message("user").write(chat_matrix_input)
        with st.spinner("Processing Token Telemetry..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        reply_string = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": reply_string})
        st.chat_message("assistant").write(reply_string)
# B. AUTOMONOMOUS NET EXPLORER NODE MODULE
elif page == "🔍 Realtime Web Crawler":
    st.markdown("""
        <div class="neobrutalist-content-card">
            <h3>REAL-TIME EXPLORATION PROTOCOLS</h3>
            <h1>🔍 WEB SEARCH MODULE</h1>
            <div class="card-narrative-paragraph">Queries active distributed network databases to aggregate and index live software framework parameters instantly.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    crawler_query_input = st.chat_input("Input focus query string fields for autonomous crawl index...")
    if crawler_query_input:
        st.session_state.search_messages.append({"role": "user", "content": crawler_query_input})
        st.chat_message("user").write(crawler_query_input)
        with st.spinner("Deploying Extraction Agents..."):
            response = agent.invoke({"messages": [{"role": "user", "content": crawler_query_input}]})
            extracted_reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": extracted_reply})
        st.chat_message("assistant").write(extracted_reply)
# C. RUNTIME CODE REFACTOR ANALYSIS LAB
elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="neobrutalist-content-card">
            <h3>LOGIC DECONSTRUCTION FRAMEWORK</h3>
            <h1>💻 CODE ANALYSIS NODE</h1>
            <div class="card-narrative-paragraph">Paste system scripts to evaluate space complexities, identify structural bugs, or generate optimal assembly refactors.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📟 Source Script Array Buffer Input")
    source_script_buffer = st.text_area("", height=220, placeholder="def compute_matrix():\n    return 'Execution Array Calibrated'")
    
    col_btn_1, col_btn_2, col_btn_3 = st.columns(3)
    with col_btn_1:
        trigger_explain = st.button("📖 EXPLAIN ARCHITECTURE", use_container_width=True)
    with col_btn_2:
        trigger_debug = st.button("🐛 AUDIT SYNTAX FAULTS", use_container_width=True)
    with col_btn_3:
        trigger_improve = st.button("⚡ OPTIMIZE PERFORMANCE", use_container_width=True)

    if source_script_buffer:
        if trigger_explain:
            with st.spinner("Mapping Call Trees..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{source_script_buffer}"}
                    ]
                )
            st.markdown('<div class="neobrutalist-content-card"><h3>📖 RECONSTRUCTED LOGIC EXPLANATION</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if trigger_debug:
            with st.spinner("Scanning for Runtime Exceptions..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{source_script_buffer}"}
                    ]
                )
            st.markdown('<div class="neobrutalist-content-card"><h3>🐛 DIAGNOSTIC CONTEXT LOGS</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if trigger_improve:
            with st.spinner("Refactoring Algorithmic Arrays..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{source_script_buffer}"}
                    ]
                )
            st.markdown('<div class="neobrutalist-content-card"><h3>⚡ PROPOSED SYSTEM OUTLINES</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Supply standard target program code into the matrix buffer text area box above to activate analytics.")
# D. TOPIC COMPREHENSION ASSESSMENT CONFIGURATOR MODULE
elif page == "📝 Examination Quiz":
    st.markdown("""
        <div class="neobrutalist-content-card">
            <h3>COMPILING COMPREHENSION METRICS</h3>
            <h1>📝 MCQ EVALUATION MATRIX</h1>
            <div class="card-narrative-paragraph">Generate multiple choice curriculum training sets dynamically from specified skill domains.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### ⚙️ Evaluation Matrix Parameters")
    target_subject_topic = st.text_input("Declare Target Subject Focus Topic Domain Tree:", placeholder="e.g. Backpropagation Math Operations")
    magnitude_questions = st.slider("Quantity of Target Examination Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE ASSESSMENT OBJECTS", use_container_width=True):
        if target_subject_topic:
            with st.spinner("Formulating Framework Schematics..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {magnitude_questions} MCQ questions about {target_subject_topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<div class="neobrutalist-content-card"><h3>🎯 TARGET GENERATED EVALUATION RUNTIMES</h3>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Missing Configuration Variable: Input focus topic domain branch parameters first.")

# E. DOCUMENT STRUCTURAL TEXT PARSER LAB
elif page == "📄 Document Structural Parser":
    st.markdown("""
        <div class="neobrutalist-content-card">
            <h3>SEMANTIC BLUEPRINT TEXT PROCESSING</h3>
            <h1>📄 STRUCTURAL FILE PARSER</h1>
            <div class="card-narrative-paragraph">Upload heavy configuration documentation packages or textbook sheets to map text values and search parameters instantly.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📁 Archive Dataset Storage Mount")
    uploaded_pdf_asset = st.file_uploader("Upload Target Technical PDF Schematic Asset:", type="pdf")
    final_extracted_pdf_text = ""
    
    if uploaded_pdf_asset:
        pdf_file_reader_instance = PyPDF2.PdfReader(io.BytesIO(uploaded_pdf_asset.read()))
        for page_index_num in pdf_file_reader_instance.pages:
            final_extracted_pdf_text += page_index_num.extract_text() or ""
        st.success("Target Content Dataset Mounted and Verified Successfully.")

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    st.write("---")
    st.write("### 📟 Context Interaction Console")
    for msg in st.session_state.pdf_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    pdf_user_query_input = st.chat_input("Query structural document fields...")
    if pdf_user_query_input:
        if not final_extracted_pdf_text.strip():
            st.warning("Data Missing Error: Please upload a valid structural manual PDF target asset first.")
        else:
            st.session_state.pdf_messages.append({"role": "user", "content": pdf_user_query_input})
            st.chat_message("user").write(pdf_user_query_input)
            
            with st.spinner("Extracting Semantic Node Elements..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"Answer the user's question accurately using only the provided document text context.\n\nContext:\n{final_extracted_pdf_text}"},
                        *st.session_state.pdf_messages
                    ]
                )
            reply_data_content = response.choices.message.content
            st.session_state.pdf_messages.append({"role": "assistant", "content": reply_data_content})
            st.chat_message("assistant").write(reply_data_content)
