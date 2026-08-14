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

# 2. CHAINGPT LABS FUTURISTIC MECHANICAL UI INJECTION (WITH ENTRY ANIMATIONS)
st.markdown("""
    <style>
    /* Keyframe Animations */
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(15px); filter: blur(4px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* Core Application Theme */
    .stApp { 
        background-color: #0f1013 !important; 
        color: #e2e8f0 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Top Navigation bar simulation */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 30px;
        background-color: #14161d;
        border-bottom: 1px solid #232631;
        margin-bottom: 25px;
        animation: fadeInSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .header-title {
        font-weight: 900;
        font-size: 20px;
        letter-spacing: 2px;
        color: #ff5500;
    }

    /* ChainGPT Tech Grid Containers */
    .tech-panel {
        background-color: #13151c !important;
        border: 1px solid #262936 !important;
        border-radius: 4px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        position: relative;
        animation: fadeInSlide 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Technical crosshair accents */
    .tech-panel::before {
        content: '+';
        position: absolute;
        top: -8px;
        left: -5px;
        color: #ff5500;
        font-size: 14px;
        font-weight: bold;
    }

    /* Typography Overrides */
    h1 { 
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: 800 !important; 
        color: #ffffff !important; 
        letter-spacing: -1px;
        text-transform: uppercase;
        margin-top: 0px !important;
    }
    h3 {
        color: #ff5500 !important;
        letter-spacing: 1px;
        font-size: 16px !important;
        text-transform: uppercase;
        margin-bottom: 15px !important;
    }
    
    /* Custom CSS Buttons styling to look like Web3 CTA Blocks */
    .stButton>button {
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid #ff5500 !important;
        border-radius: 2px !important;
        padding: 8px 20px !important;
        font-size: 12px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #ff5500 !important;
        color: #0f1013 !important;
        box-shadow: 0 0 15px rgba(255, 85, 0, 0.4);
    }

    /* Streamlit Chat Element Adjustments */
    .stChatMessage { 
        background-color: #171a24 !important; 
        border: 1px solid #242938 !important;
        border-radius: 4px !important;
        padding: 12px !important;
        animation: fadeInSlide 0.4s ease-out forwards;
    }
    
    /* Input Form fields adjustments */
    .stTextArea textarea, .stTextInput input { 
        background-color: #090a0d !important; 
        color: #ffffff !important; 
        border: 1px solid #262936 !important;
        border-radius: 2px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ff5500 !important;
    }
    
    /* Sidebar Navigation panel overrides */
    section[data-testid="stSidebar"] {
        background-color: #0a0b0e !important;
        border-right: 1px solid #1a1d26 !important;
    }
    </style>
    
    <!-- Virtual Dynamic Brand Header -->
    <div class="header-bar">
        <div class="header-title">⛓️ CHAINGPT LABS // INTERFACE</div>
        <div style="font-size:11px; color:#5a627a; letter-spacing:1px;">SYSTEM STATUS: ACTIVE</div>
    </div>
""", unsafe_allow_html=True)

# 3. BACKEND API CLIENT INITIALIZATION
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# 4. SIDEBAR NAVIGATION
st.sidebar.markdown("<h2 style='color:#ff5500; font-size:20px; letter-spacing:1px;'>🤖 OPERATING SYSTEM</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("CHOOSE MODULE:", [
    "💬 Chat",
    "🔍 Web Search Agent",
    "💻 Code Explainer",
    "📝 Quiz Generator",
    "📄 PDF Reader"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#5a627a;'>BUILT BY ROHIT • CORE ENGINE LLAMA 3</div>", unsafe_allow_html=True)
# 5. WORKSPACE INTERFACE SECTIONS
if page == "💬 Chat":
    st.markdown("""
        <div class="tech-panel">
            <h1 style="color:#ffffff;">💬 CORE CHAT SERVICES</h1>
            <p style="text-align:left; color:#6b7280; font-size:13px; margin:0;">PERSONAL PRECISE STUDY & CODING ASSISTANT COMPANION ENGINE</p>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_space, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("🗑️ RESET BUFFER"):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    st.markdown('<div class="tech-panel"><h3>📟 ACTIVE TRANSMISSION LOG</h3>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Input command or question...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("Processing Matrix Data..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "🔍 Web Search Agent":
    st.markdown("""
        <div class="tech-panel">
            <h1>🔍 WEB SEARCH AGENT</h1>
            <p style="text-align:left; color:#6b7280; font-size:13px; margin:0;">REAL-TIME INTERNET EXPLORATION AND DATA SYNTHESIS MODULE</p>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    st.markdown('<div class="tech-panel"><h3>📟 LIVE WEB STREAM</h3>', unsafe_allow_html=True)
    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    search_input = st.chat_input("Enter query parameter for live exploration...")
    if search_input:
        st.session_state.search_messages.append({"role": "user", "content": search_input})
        st.chat_message("user").write(search_input)
        with st.spinner("Invoking Web Scraping Node..."):
            response = agent.invoke({"messages": [{"role": "user", "content": search_input}]})
            reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="tech-panel">
            <h1>💻 CODE DECONSTRUCTION NODE</h1>
            <p style="text-align:left; color:#6b7280; font-size:13px; margin:0;">PASTE RUNTIME SCRIPT DATA FOR STEP-BY-STEP OPTIMIZATION</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tech-panel"><h3>📟 INPUT COMPILER</h3>', unsafe_allow_html=True)
    code_input = st.text_area("Source Code Input:", height=200, placeholder="def compute():\n    return 'Executing Matrix'")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 EXPLAIN ARCHITECTURE")
    with col2:
        debug = st.button("🐛 AUDIT ERRORS")
    with col3:
        improve = st.button("⚡ REFACTOR SCRIPT")
    st.markdown('</div>', unsafe_allow_html=True)

    if code_input:
        if explain:
            with st.spinner("Analyzing Call Stack..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="tech-panel"><h3>📖 ANALYSIS DECONSTRUCTION</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if debug:
            with st.spinner("Scanning for Exceptions..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="tech-panel"><h3>🐛 SYNTAX EXCEPTION ALERTS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        if improve:
            with st.spinner("Calculating Performance Gains..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<div class="tech-panel"><h3>⚡ COMPUTATIONAL OPTIMIZATIONS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center; color:#5a627a; font-size:12px;">▲ AWAITING TARGET COMPILE SCRIPT COMPONENT ▲</div>', unsafe_allow_html=True)
elif page == "📝 Quiz Generator":
    st.markdown("""
        <div class="tech-panel">
            <h1>📝 MCQ EVALUATION NODE</h1>
            <p style="text-align:left; color:#6b7280; font-size:13px; margin:0;">TRANSFORM RAW TOPIC PARAMETERS INTO EXAMINATION MATRIX BENCHMARKS</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tech-panel"><h3>⚙️ CONFIGURATION INTERFACE</h3>', unsafe_allow_html=True)
    topic = st.text_input("Target Evaluation Topic Domain:", placeholder="e.g. Quantum Computing, Neural Networks")
    num_questions = st.slider("Target Question Set Magnitude:", 3, 10, 5)
    generate_quiz = st.button("🎯 SYNTHESIZE EVALUATION MATRIX")
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_quiz:
        if topic:
            with st.spinner("Compiling Training Matrix..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {num_questions} MCQ questions about {topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<div class="tech-panel"><h3>🎯 TARGET RUNTIME QUIZ OBJECTS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Variable Error: Missing Topic Parameter Configuration.")

elif page == "📄 PDF Reader":
    st.markdown("""
        <div class="tech-panel">
            <h1>📄 STRUCTURAL FILE PARSER</h1>
            <p style="text-align:left; color:#6b7280; font-size:13px; margin:0;">UPLOAD ANALYTICAL CONTENT FILES FOR IN-DEPTH PARSING MODE</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tech-panel"><h3>📁 ARCHIVE DATA STORAGE INPUT</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Target Blueprint Document:", type="pdf")
    pdf_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page_num in pdf_reader.pages:
            pdf_text += page_num.extract_text()
        st.success("Configuration Matrix Verified: Content Storage Linked Ready.")
    st.markdown('</div>', unsafe_allow_html=True)

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    st.markdown('<div class="tech-panel"><h3>📟 DOCUMENT QUERY INTERFACE</h3>', unsafe_allow_html=True)
    for msg in st.session_state.pdf_messages:
        st.chat_message(msg["role"]).write(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    pdf_input = st.chat_input("Query structural document parameters here...")
    if pdf_input:
        st.session_state.pdf_messages.append({"role": "user", "content": pdf_input})
        st.chat_message("user").write(pdf_input)
        
        context_block = pdf_text if pdf_text else "No specific context dataset available."
        
        with st.spinner("Extracting Target Paragraph Context Node..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Answer the user's question accurately using only the provided document text context.\n\nContext:\n{context_block}"},
                    *st.session_state.pdf_messages
                ]
            )
        reply = response.choices[0].message.content
        st.session_state.pdf_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
