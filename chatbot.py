import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import PyPDF2
import io

# 1. EXPAND WEB WINDOW SCREEN SPACE 
st.set_page_config(
    page_title="Rohit's AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. INJECT EXACT CHAINGPT LABS WEB COMPONENT LAYOUT STYLES WITH ANIMATION 
st.markdown("""
    <style>
    /* Smooth Cascading Fluid Entry Animation */
    @keyframes techFadeIn {
        0% { opacity: 0; transform: translateY(12px); filter: blur(2px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* Core Application Background Palette Override */
    .stApp {
        background-color: #090a10 !important;
        background-image: 
            linear-gradient(to right, #141622 1px, transparent 1px),
            linear-gradient(to bottom, #141622 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
        color: #e2e8f0 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Top Horizontal Corporate Navigation Ribbon */
    .brand-top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 40px;
        background-color: #090a10;
        border-bottom: 1px solid #1c1e2e;
        margin-bottom: 30px;
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
        border-radius: 2px;
    }
    .brand-logo-text {
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: #ffffff;
        text-transform: uppercase;
    }
    .brand-logo-text span {
        color: #ff5a1f;
    }
    .brand-menu-links {
        display: flex;
        gap: 28px;
        font-size: 13px;
        color: #727b98;
        font-weight: 500;
    }
    .brand-menu-links div:hover {
        color: #ffffff;
        cursor: pointer;
    }
    .brand-cta-pill {
        background-color: #ff5a1f;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Neo-Brutalist Technical Mechanical Wireframe Content Panels */
    .chaingpt-card {
        background-color: #0d0f18 !important;
        border: 1px solid #1c1e2e !important;
        border-radius: 0px !important;
        padding: 35px !important;
        margin-bottom: 25px !important;
        position: relative;
        animation: techFadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Technical Grid Align Corner Node Markers */
    .chaingpt-card::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        width: 6px;
        height: 6px;
        border-top: 2px solid #ff5a1f;
        border-left: 2px solid #ff5a1f;
    }
    .chaingpt-card::after {
        content: '';
        position: absolute;
        bottom: -1px;
        right: -1px;
        width: 6px;
        height: 6px;
        border-bottom: 2px solid #ff5a1f;
        border-right: 2px solid #ff5a1f;
    }

    /* Headers and Content Formatting */
    h1 {
        font-size: 42px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        letter-spacing: -1px !important;
        text-transform: uppercase !important;
        margin: 0 0 15px 0 !important;
    }
    h3 {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #ff5a1f !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        margin-bottom: 12px !important;
    }
    .card-paragraph {
        font-size: 15px;
        line-height: 1.6;
        color: #727b98;
        max-width: 550px;
        margin-bottom: 25px;
    }

    /* Core Native Action Controls Customization Styling overrides */
    .stButton>button {
        background-color: #ff5a1f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 28px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(255, 90, 31, 0.2);
    }
    .stButton>button:hover {
        background-color: #e04a15 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(255, 90, 31, 0.35);
    }

    /* Chat Log Formatting Overrides */
    .stChatMessage {
        background-color: #0d0f18 !important;
        border: 1px solid #1c1e2e !important;
        border-radius: 4px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }

    /* User form standard entry boxes styling adjustment */
    .stTextArea textarea, .stTextInput input {
        background-color: #090a10 !important;
        color: #ffffff !important;
        border: 1px solid #1c1e2e !important;
        border-radius: 4px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ff5a1f !important;
    }

    /* Left Sidebar Menu Framework Overrides */
    section[data-testid="stSidebar"] {
        background-color: #06070b !important;
        border-right: 1px solid #141622 !important;
    }
    </style>

    <!-- Top Static ChainGPT Navigation Shell Mockup -->
    <div class="brand-top-nav">
        <div class="brand-logo-wrap">
            <div class="brand-orange-cube"></div>
            <div class="brand-logo-text">ROHIT LABS<span>//</span>AI</div>
        </div>
        <div class="brand-menu-links">
            <div>Our Programs</div>
            <div>Portfolio</div>
            <div>Media</div>
            <div>Reviews</div>
            <div>Team</div>
            <div>FAQ</div>
        </div>
        <div class="brand-cta-pill">Apply Now</div>
    </div>
""", unsafe_allow_html=True)

# 3. CONVERT ACTIVE ENVIRONMENT CONNECTIONS
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

llm = ChatGroq(
    api_key=api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)
search = DuckDuckGoSearchRun()
tools = [search]
agent = create_react_agent(llm, tools)

# 4. SIDEBAR SELECTION SYSTEM
st.sidebar.markdown("<h3 style='margin-top:10px;'>🧭 MODULE DIRECTORY</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("CHOOSE INSTANCE:", [
    "💬 Chat",
    "🔍 Web Search Agent",
    "💻 Code Explainer",
    "📝 Quiz Generator",
    "📄 PDF Reader"
])
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:11px; color:#4a4f66;'>BUILT BY ROHIT • RUNNING LLAMA COMPILER</div>", unsafe_allow_html=True)
# 5. RENDER APPLICATION INTERFACE TARGET LOGIC
if page == "💬 Chat":
    st.markdown("""
        <div class="chaingpt-card">
            <h3>BACKING THE FUTURE</h3>
            <h1>AI CHAT COMPANION</h1>
            <div class="card-paragraph">Your personal decentralized space for technical study, rapid conceptual brainstorming, structural engineering updates, and direct curriculum navigation.</div>
        </div>
    """, unsafe_allow_html=True)

    system_prompt = """You are Rohit's personal AI Study & Coding Assistant.
You help with programming, AI/ML concepts, debugging code, and BTech subjects.
You explain things simply and clearly, like a smart friend who knows everything about tech.
You are encouraging, friendly, and always push the user to learn and grow.
Keep responses concise and practical."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    col_empty, col_action = st.columns([5, 1])
    with col_action:
        if st.button("🪹 WIPE STORAGE"):
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            st.rerun()

    # Chat context box
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Enter conversational string payload...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        with st.spinner("Compiling Token Sequence..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "🔍 Web Search Agent":
    st.markdown("""
        <div class="chaingpt-card">
            <h3>REALTIME DATA PARSING</h3>
            <h1>WEB SEARCH AGENT</h1>
            <div class="card-paragraph">Advanced scraping intelligence tracking live parameters across open networks to extract real-time web infrastructure records instantly.</div>
        </div>
    """, unsafe_allow_html=True)

    if "search_messages" not in st.session_state:
        st.session_state.search_messages = []

    for msg in st.session_state.search_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    search_input = st.chat_input("Input live target network search query parameter...")
    if search_input:
        st.session_state.search_messages.append({"role": "user", "content": search_input})
        st.chat_message("user").write(search_input)
        with st.spinner("Executing Network Crawl Nodes..."):
            response = agent.invoke({"messages": [{"role": "user", "content": search_input}]})
            reply = response["messages"][-1].content
        st.session_state.search_messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

elif page == "💻 Code Explainer":
    st.markdown("""
        <div class="chaingpt-card">
            <h3>OPTIMIZATION RUNTIME</h3>
            <h1>CODE DECONSTRUCTION</h1>
            <div class="card-paragraph">Submit script telemetry algorithms for step-by-step logic tracing, algorithmic optimization, and system syntax auditing.</div>
        </div>
    """, unsafe_allow_html=True)

    code_input = st.text_area("Source Code Array Buffer Input:", height=220, placeholder="def active_matrix():\n    print('Grid Operational')")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("📖 EXPLAIN LOGIC")
    with col2:
        debug = st.button("🐛 AUDIT EXCEPTIONS")
    with col3:
        improve = st.button("⚡ REFACTOR SCRIPT")

    if code_input:
        if explain:
            with st.spinner("Parsing Function Stack..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert coding assistant. Explain code simply and clearly."},
                        {"role": "user", "content": f"Explain this code step by step:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>📖 ANALYSIS BREAKDOWN</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)

        if debug:
            with st.spinner("Analyzing Stack Overflows..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Find bugs and errors in code."},
                        {"role": "user", "content": f"Find any bugs or errors in this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>🐛 SYNTAX TRACKER ERROR DIAGNOSTICS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)

        if improve:
            with st.spinner("Computing Compute Complexities..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer. Suggest improvements to code."},
                        {"role": "user", "content": f"Suggest improvements for this code:\n\n{code_input}"}
                    ]
                )
            st.markdown('<h3>⚡ PROPOSED OPTIMIZATION REFACTORS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
elif page == "📝 Quiz Generator":
    st.markdown("""
        <div class="chaingpt-card">
            <h3>TRANSFORMING KNOWLEDGE</h3>
            <h1>EVALUATION GENERATOR</h1>
            <div class="card-paragraph">Synthesize highly structured Multiple Choice training frameworks directly from plain instructional topic domains.</div>
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter Target Skill Domain Framework:", placeholder="e.g., Backpropagation Calculus, Graph Databases")
    num_questions = st.slider("Quantity of Target Evaluation Nodes:", 3, 10, 5)

    if st.button("🎯 SYNTHESIZE ASSESSMENT MATRIX"):
        if topic:
            with st.spinner("Generating Target Quiz Objects..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher. Generate clear MCQ questions with 4 options and correct answers."},
                        {"role": "user", "content": f"Generate {num_questions} MCQ questions about {topic}. Format each question with 4 options (A, B, C, D) and mark the correct answer at the end."}
                    ]
                )
            st.markdown('<h3>🎯 TARGET TRAINING EVALUATION SCHEMATICS</h3>', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
        else:
            st.warning("Missing Configuration Parameter: Please declare evaluation target branch.")

elif page == "📄 PDF Reader":
    st.markdown("""
        <div class="chaingpt-card">
            <h3>DOCUMENT RECONSTRUCTION</h3>
            <h1>STRUCTURAL FILE PARSER</h1>
            <div class="card-paragraph">Upload complex analytic data payloads or technical blueprints to query underlying context datasets immediately.</div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Target System Document Package:", type="pdf")
    pdf_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page_num in pdf_reader.pages:
            pdf_text += page_num.extract_text()
        st.success("Configuration Matrix Verified: Target Context Content Synced.")

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    for msg in st.session_state.pdf_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    pdf_input = st.chat_input("Query structural document parameters here...")
    if pdf_input:
        st.session_state.pdf_messages.append({"role": "user", "content": pdf_input})
        st.chat_message("user").write(pdf_input)
        
        context_block = pdf_text if pdf_text else "No specific context dataset available."
        
        with st.spinner("Running Semantic Context Analysis..."):
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
