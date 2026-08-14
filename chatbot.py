import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io
import time

# =============================================================================
# 1. APPLICATION ENGINE ENVIRONMENT LAYOUT CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. BRAND STYLE CONFIGURATION METRICS (CHAINGPT LABS MESH LAYERS)
# =============================================================================
st.markdown("""
    <style>
    /* Premium Hardware Accelerated Keyframe Layers */
    @keyframes cyberFadeSlideIn {
        0% { opacity: 0; transform: translateY(30px); filter: blur(6px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @keyframes structuralPulse {
        0% { opacity: 0.15; }
        50% { opacity: 0.35; }
        100% { opacity: 0.15; }
    }
    @keyframes particleShift {
        0% { background-position: 0px 0px; }
        100% { background-position: 80px 80px; }
    }

    /* Core Structural Architecture Canvas Blueprint Grid Background */
    .stApp {
        background-color: #e6e8eb !important;
        background-image: 
            linear-gradient(to right, #ccd2db 1px, transparent 1px),
            linear-gradient(to bottom, #ccd2db 1px, transparent 1px) !important;
        background-size: 80px 80px !important;
        color: #0f1115 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }

    /* Gateway Landing Component Framework Styling */
    .telemetry-landing-wrapper {
        text-align: center;
        margin-top: 15vh;
        padding: 40px;
        animation: cyberFadeSlideIn 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .telemetry-tagline {
        font-size: 14px;
        font-weight: 800;
        color: #ff5a1f;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .telemetry-title {
        font-size: 96px;
        font-weight: 900;
        color: #0f1115;
        letter-spacing: -4px;
        text-transform: uppercase;
        line-height: 0.9;
        margin-bottom: 12px;
    }
    .telemetry-subtitle {
        font-size: 18px;
        font-weight: 600;
        color: #555e72;
        letter-spacing: 1px;
        margin-bottom: 60px;
    }

    /* Top Horizontal Corporate Navigation Component */
    .premium-top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 45px;
        background-color: #e6e8eb;
        border-bottom: 2px solid #b8bfc9;
        margin-bottom: 0px;
        animation: cyberFadeSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .premium-logo-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .premium-orange-block {
        width: 14px;
        height: 14px;
        background-color: #ff5a1f;
    }
    .premium-logo-string {
        font-size: 16px;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #0f1115;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Neo-Brutalist Layout Content Panel Modules */
    .blueprint-panel-card {
        background-color: #edf0f4 !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 45px !important;
        margin-bottom: 35px !important;
        position: relative;
        box-shadow: 6px 6px 0px #0f1115 !important;
        animation: cyberFadeSlideIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Crosshair Structural Corner Alignment Markers */
    .blueprint-panel-card::before {
        content: '';
        position: absolute;
        top: -6px;
        left: -6px;
        width: 10px;
        height: 10px;
        background-color: #ff5a1f;
        border: 2px solid #0f1115;
    }
    .blueprint-panel-card::after {
        content: '';
        position: absolute;
        bottom: -6px;
        right: -6px;
        width: 10px;
        height: 10px;
        background-color: #ff5a1f;
        border: 2px solid #0f1115;
    }

    /* Core Document Header Typography Resets */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 48px !important;
        font-weight: 900 !important;
        color: #0f1115 !important;
        letter-spacing: -1.5px !important;
        text-transform: uppercase !important;
        margin-top: 0px !important;
        margin-bottom: 15px !important;
    }
    h2 {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0f1115 !important;
        text-transform: uppercase !important;
    }
    h3 {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #ff5a1f !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        margin-bottom: 10px !important;
    }
    .panel-narrative {
        font-size: 16px;
        line-height: 1.6;
        color: #555e72;
        margin-bottom: 30px;
    }

    /* Web3 Custom Solid Control Buttons */
    .stButton>button {
        background-color: #ff5a1f !important;
        color: #ffffff !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 16px 36px !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
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

    /* Functional Form Input Element Customization Blocks */
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        color: #0f1115 !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        font-family: monospace !important;
        padding: 15px !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ff5a1f !important;
        box-shadow: none !important;
    }

    /* Tailored Layout Chat Output Elements */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 2px solid #0f1115 !important;
        border-radius: 0px !important;
        padding: 22px !important;
        margin-bottom: 16px !important;
        box-shadow: 4px 4px 0px rgba(15, 17, 21, 0.05) !important;
    }

    /* Navigation Sidebar Overrides Wrapper */
    section[data-testid="stSidebar"] {
        background-color: #dcdee4 !important;
        border-right: 3px solid #0f1115 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 3. SECURE ENDPOINT HARDWARE API CONNECT AGENTS
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
# 4. SECURE RUNTIME ACCESS KEY LOGIC
# =============================================================================
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False

# Gateway Authorization Verification Dashboard Overlay
if not st.session_state.app_unlocked:
    st.markdown("""
        <div class="telemetry-landing-wrapper">
            <div class="telemetry-tagline">INITIALIZING CORE ACCESS SEGMENT PROTOCOLS</div>
            <div class="telemetry-title">KUBOOM CHATBOT</div>
            <div class="telemetry-subtitle">A chatbot made by Rohit</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_layout_l, col_layout_btn, col_layout_r = st.columns([1, 1.4, 1])
    with col_layout_btn:
        if st.button("INITIALIZE WORKSPACE MODULES 🚀", use_container_width=True):
            st.session_state.app_unlocked = True
            st.rerun()
    st.stop()

# =============================================================================
# 5. WORKSPACE TOP LINK NAVIGATION RUNTIME FRAME
# =============================================================================
st.markdown("""
    <div class="premium-top-nav">
        <div class="premium-logo-group">
            <div class="premium-orange-block"></div>
            <div class="premium-logo-string">WELCOME TO ROHIT'S CHATBOT</div>
        </div>
        <a style="
            display: inline-block;
            background-color: #0f1115;
            color: #ffffff !important;
            font-size: 11px;
            font-weight: 800;
            padding: 12px 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 2px solid #0f1115;
            border-radius: 0px;
            text-decoration: none !important;
            box-shadow: 4px 4px 0px #ff5a1f;
        " href="https://github.io" target="_blank">🔗 VIEW PORTFOLIO</a>
    </div>
    <div style="margin-bottom: 40px;"></div>
""", unsafe_allow_html=True)

# Sidebar selection routing parameters
st.sidebar.markdown("<h3 style='margin-top:10px;'>⚙️ UTILITY FRAMEWORK</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat Matrix",
    "🔍 Realtime Web Crawler",
    "💻 Code Explainer",
    "📝 Examination Quiz",
    "📄 Document Structural Parser"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#555e72; font-weight:700;'>BUILT BY ROHIT • RUNNING LLAMA ENGINES</div>", unsafe_allow_html=True)
# =============================================================================
# 6. INSTANCE CONTROL COMPILER LOGIC
# =============================================================================

# A. CHAT SERVICES ENTRY SEGMENT
if page == "💬 Chat Matrix":
    st.markdown("""
        <div class="blueprint-panel-card">
            <h3>CORE CONVERSATIONAL MATRIX</h3>
            <h1>💬 CORE CHAT SERVICES</h1>
            <div class="panel-narrative">Direct low-latency telemetry terminal providing comprehensive query assistance for engineering subjects, logic architecture, and technical frameworks.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_empty_space, col_reset_action = st.columns([3.5, 1.5])
    with col_reset_action:
        if st.button("🗑️ CLEAR INSTANCE MEMORY", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    # Dynamic tracking arrays logic loop
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    chat_query = st.chat_input("Enter conversational string payload blocks...")
    if chat_query:
        st.session_state.messages.append({"role": "user", "content": chat_query})
        st.chat_message("user").write(chat_query)
        with st.spinner("Extracting Token Matrix Values..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        ai_reply = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").write(ai_reply)
# B. AUTONOMOUS NETWORK SCRAPER SEARCH ENGINE MODULE
elif page == "🔍 Realtime Web Crawler":
    st.markdown("""
        <div class="blueprint-panel-card">
            <h3>REAL-TIME SCRAPING DISCOVERY NODES</h3>
            <h1>🔍 WEB SEARCH AGENT</h1>
            <div class="panel-narrative">Runs real-time web exploration scripts to crawl active global databases and cross-reference records against core engineering documentation.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    crawler_input = st.chat_input("Input focus parameter query strings for live indexing...")
    if crawler_input:
        st.session_state.search_messages.append({"role": "user", "content": crawler_input})
        st.chat_message("user").write(crawler_input)
        with st.spinner("Triggering Network Scrape Arrays..."):
            response = agent.invoke({"messages": [{"role": "user", "content": crawler_input}]})
            crawler_reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": crawler_reply})
        st.chat_message("assistant").write(crawler_reply)
# C. RUNTIME SCRIPT ANALYSIS DIAGNOSTICS LAB
elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="blueprint-panel-card">
            <h3>OPTIMIZATION REFACTOR COMPILER</h3>
            <h1>💻 CODE DECONSTRUCTION NODE</h1>
            <div class="panel-narrative">Paste script elements to audit memory space complexities, identify syntax structural bugs, or generate performant refactors.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📟 Source Script Array Buffer Input")
    source_code_input = st.text_area("", height=220, placeholder="def compute_matrix():\n    return 'System Calibrated'")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    with col_act1:
        explain_btn = st.button("📖 EXPLAIN PATTERNS", use_container_width=True)
    with col_act2:
        debug_btn = st.button("🐛 DIAGNOSE EXCEPTIONS", use_container_width=True)
    with col_act3:
        improve_btn = st.button("⚡ REFACTOR SCRIPT", use_container_width=True)

    if source_code_input:
        if explain_btn:
            with st.spinner("Parsing Call Stack Trees..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{source_code_input}"}
                    ]
                )
            st.markdown('<h2>📖 DECONSTRUCTED LOGIC REGISTERS</h2>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if debug_btn:
            with st.spinner("Analyzing Stack Overflows..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{source_code_input}"}
                    ]
                )
            st.markdown('<h2>🐛 CONTEXT EXCEPTIONS TRACKING LOG</h2>', unsafe_allow_html=True)
            st.write(response.choices.message.content)

        if improve_btn:
            with st.spinner("Calculating Performance Gains..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{source_code_input}"}
                    ]
                )
            st.markdown('<h2>⚡ RECOMMENDED SYSTEM OPTIMIZATIONS</h2>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
    else:
        st.info("👆 Paste targeted code parameters into the textarea box above to activate compiler insights.")
# D. TOPIC COMPREHENSION EXAMINATION MATRIX GENERATOR
elif page == "📝 Examination Quiz":
    st.markdown("""
        <div class="blueprint-panel-card">
            <h3>COMPILING COMPREHENSION OBJECTS</h3>
            <h1>📝 MCQ TASK FIELD GENERATOR</h1>
            <div class="panel-narrative">Convert target textbook subjects or complex documentation headings into structural multiple-choice training sets.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### ⚙️ Evaluation Matrix Parameters")
    target_topic = st.text_input("Declare Target Subject Focus Domain Tree:", placeholder="e.g., Deep Convolutional Neural Layers")
    selected_magnitude = st.slider("Quantity of Target Examination Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE ASSESSMENT BLOCKS", use_container_width=True):
        if target_topic:
            with st.spinner("Formulating Training Objects..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {selected_magnitude} MCQ questions about {target_topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<h2>🎯 COMPILED ASSESSMENT METRICS</h2>', unsafe_allow_html=True)
            st.write(response.choices.message.content)
        else:
            st.warning("Missing Configuration Input: Specify evaluation topic parameters first.")

# E. STRUCTURAL FILE PARSING RECONSTRUCTION MODULE
elif page == "📄 Document Structural Parser":
    st.markdown("""
        <div class="blueprint-panel-card">
            <h3>SEMANTIC BLUEPRINT DATA INTERROGATION</h3>
            <h1>📄 STRUCTURAL FILE PARSER</h1>
            <div class="panel-narrative">Process analytical context sheets or layout documentation packages to map underlying text strings and run instant queries.</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📁 Archive Dataset Storage Mount")
    uploaded_pdf_file = st.file_uploader("Upload Target Technical PDF Schematic:", type="pdf")
    extracted_pdf_text = ""
    
    if uploaded_pdf_file:
        pdf_file_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_pdf_file.read()))
        for page_index in pdf_file_reader.pages:
            extracted_pdf_text += page_index.extract_text() or ""
        st.success("Configuration Matrix Verified: Content Repository Mounted Successfully.")

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    st.write("---")
    st.write("### 📟 Context Interaction Console")
    for msg in st.session_state.pdf_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    pdf_user_query = st.chat_input("Query structural document parameters here...")
    if pdf_user_query:
        if not extracted_pdf_text.strip():
            st.warning("Data Missing Error: Please upload a readable PDF schematic target asset package first.")
        else:
            st.session_state.pdf_messages.append({"role": "user", "content": pdf_user_query})
            st.chat_message("user").write(pdf_user_query)
            
            with st.spinner("Extracting Semantic Paragraph Node Context..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"Answer the user's question accurately using only the provided document text context.\n\nContext:\n{extracted_pdf_text}"},
                        *st.session_state.pdf_messages
                    ]
                )
            pdf_ai_reply = response.choices.message.content
            st.session_state.pdf_messages.append({"role": "assistant", "content": pdf_ai_reply})
            st.chat_message("assistant").write(pdf_ai_reply)
