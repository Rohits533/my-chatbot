import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io
import time
import datetime

# =============================================================================
# 1. CORE STREAMLIT INSTANCE INITIALIZATION & ARCHITECTURE OVERRIDES
# =============================================================================

st.set_page_config(
page_title="Rohit's AI Assistant",
page_icon="🤖",
layout="wide",
initial_sidebar_state="expanded"
)

# =============================================================================
# 2. BRAND STYLE CONFIGURATION METRICS (CHAINGPT LABS GLOWING LASER GRID)
# =============================================================================

st.markdown("""
<style>
/* Advanced Accelerated Keyframe CSS Animation Engine */
@keyframes entranceZoomFade {
0% { opacity: 0; transform: scale(0.95) translateY(40px); filter: blur(12px); }
50% { opacity: 0.4; filter: blur(6px); }
100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
}
@keyframes fluidPanelSlideIn {
0% { opacity: 0; transform: translateY(30px); filter: blur(6px); }
100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}
@keyframes orangeLaserScroll {
0% { background-position: 0px 0px, 0px 0px; }
100% { background-position: 120px 120px, -60px 60px; }
}
@keyframes matrixPulseGlow {
0% { border-color: rgba(255, 90, 31, 0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
50% { border-color: rgba(255, 90, 31, 0.6); box-shadow: 0 4px 30px rgba(255, 90, 31, 0.15); }
100% { border-color: rgba(255, 90, 31, 0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
}

/* Core Structural Architecture Canvas Blueprint Grid Background */
.stApp {
    background-color: #0d0f14 !important;
    background-image: 
        linear-gradient(to right, rgba(255, 90, 31, 0.12) 2px, transparent 2px),
        linear-gradient(to bottom, rgba(255, 90, 31, 0.12) 2px, transparent 2px),
        radial-gradient(circle at 50% 50%, rgba(255, 90, 31, 0.05) 0%, transparent 80%) !important;
    background-size: 60px 60px, 60px 60px, 100% 100% !important;
    color: #e2e8f0 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif !important;
    animation: orangeLaserScroll 20s linear infinite !important;
}

/* Gateway Landing Component Framework Styling */
.telemetry-landing-wrapper {
    text-align: center;
    margin-top: 10vh;
    padding: 60px;
    background-color: rgba(13, 15, 20, 0.9);
    border: 2px solid rgba(255, 90, 31, 0.3);
    border-radius: 0px;
    backdrop-filter: blur(15px);
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 0 50px rgba(255, 90, 31, 0.2);
    position: relative;
    animation: entranceZoomFade 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.telemetry-landing-wrapper::before {
    content: ''; position: absolute; top: -5px; left: -5px; width: 10px; height: 10px; background-color: #ff5a1f;
}
.telemetry-landing-wrapper::after {
    content: ''; position: absolute; bottom: -5px; right: -5px; width: 10px; height: 10px; background-color: #ff5a1f;
}
.telemetry-tagline {
    font-size: 14px;
    font-weight: 800;
    color: #ff5a1f;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 25px;
}
.telemetry-title {
    font-size: 96px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -3px;
    text-transform: uppercase;
    line-height: 0.9;
    margin-bottom: 15px;
}
.telemetry-subtitle {
    font-size: 19px;
    font-weight: 600;
    color: #8fa0be;
    letter-spacing: 1px;
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
padding: 22px 50px;
background-color: rgba(13, 15, 20, 0.95);
border-bottom: 2px solid rgba(255, 90, 31, 0.3);
margin-bottom: 0px;
backdrop-filter: blur(10px);
animation: fluidPanelSlideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
box-shadow: 0 0 12px #ff5a1f;
}
.brand-logo-text-string {
font-size: 16px;
font-weight: 900;
letter-spacing: 1.5px;
color: #ffffff;
text-transform: uppercase;
}

/* Neo-Brutalist Technical Panel Workspace Shell Modules */
.neobrutalist-content-card {
    background-color: rgba(19, 22, 31, 0.92) !important;
    border: 2px solid rgba(255, 90, 31, 0.2) !important;
    border-radius: 0px !important;
    padding: 50px !important;
    margin-bottom: 40px !important;
    position: relative;
    backdrop-filter: blur(12px);
    animation: fluidPanelSlideIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-name: matrixPulseGlow;
    animation-duration: 4s;
    animation-iteration-count: infinite;
}
.neobrutalist-content-card::before {
    content: ''; position: absolute; top: -5px; left: -5px; width: 10px; height: 10px; background-color: #ff5a1f;
}
.neobrutalist-content-card::after {
    content: ''; position: absolute; bottom: -5px; right: -5px; width: 10px; height: 10px; background-color: #ff5a1f;
}

/* Core Native Elements Typographical Configurations Overrides */
h1 {
    font-size: 48px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    letter-spacing: -1.5px !important;
    text-transform: uppercase !important;
    margin-top: 0px !important;
    margin-bottom: 15px !important;
}
h2 { font-size: 26px !important; font-weight: 800 !important; color: #ffffff !important; text-transform: uppercase !important; }
h3 { font-size: 13px !important; font-weight: 800 !important; color: #ff5a1f !important; text-transform: uppercase !important; letter-spacing: 3px !important; margin-bottom: 12px !important; }
.card-narrative-paragraph { font-size: 16px; line-height: 1.6; color: #8fa0be; margin-bottom: 30px; }

/* Premium Block Core Buttons Customization Layout */
.stButton>button {
    background-color: #ff5a1f !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 90, 31, 0.5) !important;
    border-radius: 0px !important;
    padding: 16px 40px !important;
    font-size: 13px !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    box-shadow: 0 4px 15px rgba(255, 90, 31, 0.25) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    width: 100% !important;
}
.stButton>button:hover {
    background-color: #ffffff !important;
    color: #0d0f14 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 30px rgba(255, 95, 31, 0.7) !important;
    transform: translateY(-2px) !important;
}

/* Functional Processing Form Elements Styling Customization */
.stTextArea textarea, .stTextInput input {
    background-color: #161a24 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 90, 31, 0.3) !important;
    border-radius: 0px !important;
    font-family: monospace !important;
    padding: 16px !important;
    font-size: 14px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #ff5a1f !important;
    box-shadow: 0 0 12px rgba(255, 90, 31, 0.4) !important;
}

/* High-End Dark Workspace Chat Logs Layout */
.stChatMessage {
    background-color: #141722 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 90, 31, 0.25) !important;
    border-radius: 0px !important;
    padding: 24px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
    animation: fluidPanelSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Left Sidebar Global Panel Formats Intercept */
section[data-testid="stSidebar"] {
    background-color: #08090d !important;
    border-right: 2px solid rgba(255, 90, 31, 0.3) !important;
}
section[data-testid="stSidebar"] .stRadio label p {
    color: #8fa0be !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
</style>

""", unsafe_allow_html=True)

# =============================================================================
# 3. SECURE REPOSITORY BACKEND CLIENT INTEGRATIONS & TELEMETRY INITIALIZATION
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
    <div class="telemetry-landing-wrapper">
    <div class="telemetry-tagline">INITIALIZING ACCESS INSTANCE PROTOCOLS</div>
    <div class="telemetry-title">KUBOOM CHATBOT</div>
    <div class="telemetry-subtitle">A chatbot made by Rohit</div>
    </div>
    """, unsafe_allow_html=True)

    col_entry_l, col_entry_btn, col_entry_r = st.columns([1, 1.4, 1])
    with col_entry_btn:
        if st.button("LAUNCH WORKSPACE ENGINES 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()

# =============================================================================
# 5. GLOBAL HORIZONTAL BRAND SYSTEM RIBBON NAVIGATION
# =============================================================================

st.markdown("""
<div class="brand-navigation-ribbon">
<div class="brand-logo-cluster">
<div class="brand-orange-block"></div>
<div class="brand-logo-text-string">WELCOME TO ROHIT'S CHATBOT</div>
</div>
<a style="
         display: inline-block;
         background-color: #ff5a1f;
         color: #ffffff !important;
         font-size: 11px;
         font-weight: 800;
         padding: 12px 24px;
         text-transform: uppercase;
         letter-spacing: 1.5px;
         border: none;
         border-radius: 0px;
         text-decoration: none !important;
         box-shadow: 0 4px 15px rgba(255, 90, 31, 0.4);
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
"📝 Quiz Matrix",
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
    <div class="card-narrative-paragraph">Direct pipeline into raw Llama processing layers optimized for engineering concepts, advanced BTech topics, and framework tutorials.</div>
    </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.

You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    # Structural Telemetry Layout Grid Row
    st.write("### 📊 Workspace Performance Records")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric(label="ACTIVE PROCESSING CORE", value="Llama 3.3 70B")
    with col_stat2:
        st.metric(label="ACTIVE STORAGE FLOWS", value=f"{len(st.session_state.messages) - 1} Signals")
    with col_stat3:
        if st.button("🗑️ PURGE MEMORY PACKETS", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    st.write("---")
    st.write("### 📟 Transaction Streams Log")

    # Render conversational logs
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    chat_matrix_input = st.chat_input("Enter message packet strings or curriculum queries...")
    if chat_matrix_input:
        st.session_state.messages.append({"role": "user", "content": chat_matrix_input})
        st.chat_message("user").write(chat_matrix_input)
        
        with st.spinner("Processing Matrix Data..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        reply_string = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply_string})
        st.chat_message("assistant").write(reply_string)

# B. AUTONOMOUS NETWORK SCRAPER SEARCH ENGINE MODULE
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

    # Local Metric Telemetry Tracking Dashboard Rows
    st.write("### 📊 Live Scraper Telemetry Metrics")
    col_crawl_1, col_crawl_2, col_crawl_3 = st.columns(3)
    with col_crawl_1:
        st.metric(label="EXTRACTION SEARCH CORE", value="DuckDuckGo Node")
    with col_crawl_2:
        st.metric(label="ACTIVE STREAM SESSIONS", value=f"{len(st.session_state.search_messages)} Buffers")
    with col_crawl_3:
        if st.button("🗑️ RESET LIVE CRAWL STREAM", use_container_width=True):
            st.session_state.search_messages = []
            st.rerun()

    st.write("---")
    st.write("### 📟 Live Web Stream")
    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    crawler_query_input = st.chat_input("Input focus query string fields for autonomous crawl index...")
    if crawler_query_input:
        st.session_state.search_messages.append({"role": "user", "content": crawler_query_input})
        st.chat_message("user").write(crawler_query_input)
        
        with st.spinner("Deploying Extraction Agents Across Networks..."):
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

    # Architectural Telemetry Dashboard Rows
    st.write("### 📊 Compiler Diagnostic Parameters")
    col_code_1, col_code_2, col_code_3 = st.columns(3)
    with col_code_1:
        st.metric(label="PARSER COMPILER ENGINE", value="Llama-3.3-70B")
    with col_code_2:
        st.metric(label="MAX COMPUTE LIMIT", value="8,192 Tokens")
    with col_code_3:
        st.metric(label="SYSTEM LATENCY STATUS", value="OPTIMAL // 0.02s")

    st.write("---")
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
            st.write(response.choices[0].message.content)
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
            st.write(response.choices[0].message.content)
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
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Supply standard target program code into the matrix buffer text area box above to activate analytics.")

# D. TOPIC COMPREHENSION ASSESSMENT CONFIGURATOR MODULE
elif page == "📝 Quiz Matrix":
    st.markdown("""
    <div class="neobrutalist-content-card">
    <h3>COMPILING COMPREHENSION METRICS</h3>
    <h1>📝 MCQ EVALUATION MATRIX</h1>
    <div class="card-narrative-paragraph">Generate multiple choice curriculum training sets dynamically from specified skill domains.</div>
    </div>
    """, unsafe_allow_html=True)

    # Local Telemetry Dashboard Rows
    st.write("### 📊 Quiz Evaluation Metrics")
    col_quiz_1, col_code_2, col_code_3 = st.columns(3)
    with col_quiz_1:
        st.metric(label="EVALUATION COMPILER", value="Llama-3.3-70B")
    with col_code_2:
        st.metric(label="TARGET GRADING SYSTEM", value="BTech / Bounded")
    with col_code_3:
        st.metric(label="SCHEMA COMPLIANCE STATUS", value="100% SECURE")

    st.write("---")
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
            st.write(response.choices[0].message.content)
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

    # Structural Telemetry Layout Grid Row
    st.write("### 📊 Document Mounting Metrics")
    col_pdf_1, col_pdf_2, col_pdf_3 = st.columns(3)
    with col_pdf_1:
        st.metric(label="PARSER BUFFER TYPE", value="PyPDF2 Engine")
    with col_pdf_2:
        st.metric(label="DATA INPUT STATUS", value="READY FOR MOUNT")
    with col_pdf_3:
        if st.button("🗑️ PURGE DOCUMENT CONTEXT", use_container_width=True):
            st.session_state.pdf_messages = []
            st.rerun()

    st.write("---")
    st.write("### 📁 Archive Data Storage Mount")
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
            reply_data_content = response.choices[0].message.content
            st.session_state.pdf_messages.append({"role": "assistant", "content": reply_data_content})
            st.chat_message("assistant").write(reply_data_content)
