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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --bg:#07090f; --panel:rgba(17,21,32,.84); --panel2:rgba(22,27,41,.94);
  --border:rgba(255,255,255,.08); --purple:#8b5cf6; --blue:#3b82f6;
  --text:#f7f8fc; --muted:#8d96aa;
}
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:"DM Sans",-apple-system,BlinkMacSystemFont,sans-serif}
.stApp{
  background:radial-gradient(circle at 12% 0%,rgba(139,92,246,.14),transparent 30%),
             radial-gradient(circle at 90% 12%,rgba(59,130,246,.10),transparent 28%),
             linear-gradient(180deg,#080a11,#060810);color:var(--text)
}
.stApp:before{
  content:"";position:fixed;inset:0;pointer-events:none;opacity:.45;
  background-image:linear-gradient(rgba(255,255,255,.016) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.016) 1px,transparent 1px);
  background-size:56px 56px;mask-image:linear-gradient(to bottom,black,transparent 80%)
}
section[data-testid="stSidebar"]{background:rgba(8,10,17,.96)!important;border-right:1px solid var(--border)!important}
section[data-testid="stSidebar"]>div{padding:22px 15px}
section[data-testid="stSidebar"] .stRadio>div{gap:6px}
section[data-testid="stSidebar"] .stRadio label{border:1px solid transparent;border-radius:12px;padding:9px 11px;transition:.2s}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(255,255,255,.04);border-color:var(--border)}
h1,h2,h3{font-family:"Space Grotesk",sans-serif!important;text-transform:none!important;letter-spacing:-.03em!important}
h1{font-size:42px!important} h2{font-size:28px!important}
h3{font-size:12px!important;letter-spacing:.12em!important;color:#a78bfa!important}
button,[data-testid="stButton"] button{
  border-radius:11px!important;border:1px solid rgba(255,255,255,.1)!important;
  background:linear-gradient(135deg,#8b5cf6,#6366f1)!important;color:#fff!important;
  font-weight:700!important;min-height:44px;transition:.18s!important
}
button:hover,[data-testid="stButton"] button:hover{transform:translateY(-1px);box-shadow:0 12px 30px rgba(99,102,241,.25)!important}
.stTextInput input,.stTextArea textarea{
  background:rgba(11,14,23,.92)!important;color:#fff!important;
  border:1px solid var(--border)!important;border-radius:12px!important;padding:13px 15px!important
}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:rgba(139,92,246,.5)!important;box-shadow:0 0 0 3px rgba(139,92,246,.1)!important}
[data-testid="stChatMessage"]{
  background:rgba(15,19,29,.76)!important;border:1px solid var(--border)!important;
  border-radius:16px!important;padding:16px 18px!important;margin:10px 0!important
}
[data-testid="stMetric"]{
  background:linear-gradient(145deg,rgba(20,25,38,.9),rgba(13,16,26,.86));
  border:1px solid var(--border);border-radius:15px;padding:16px
}
[data-testid="stMetricLabel"]{color:var(--muted)!important}
[data-testid="stMetricValue"]{color:#fff!important;font-family:"Space Grotesk",sans-serif}
div[data-testid="stFileUploader"]{background:rgba(13,17,27,.8);border:1px dashed rgba(139,92,246,.35);border-radius:14px;padding:8px}
.topbar{
  display:flex;justify-content:space-between;align-items:center;padding:14px 18px;margin-bottom:28px;
  border:1px solid var(--border);border-radius:16px;background:rgba(10,13,21,.76);backdrop-filter:blur(18px)
}
.brand{display:flex;align-items:center;gap:11px}.brand-mark{
  width:34px;height:34px;border-radius:10px;display:grid;place-items:center;
  background:linear-gradient(135deg,#8b5cf6,#3b82f6);box-shadow:0 8px 28px rgba(99,102,241,.25)
}
.brand-name{font-family:"Space Grotesk";font-weight:700}.brand-sub{color:var(--muted);font-size:11px}
.status{display:flex;align-items:center;gap:8px;color:#aeb6c8;font-size:12px;border:1px solid var(--border);padding:8px 11px;border-radius:999px}
.dot{width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 12px #34d399}
.hero{
  padding:54px 34px;border:1px solid var(--border);border-radius:24px;
  background:radial-gradient(circle at 80% 20%,rgba(99,102,241,.17),transparent 30%),
             linear-gradient(145deg,rgba(19,24,38,.94),rgba(10,13,22,.92));
  box-shadow:0 30px 90px rgba(0,0,0,.25);text-align:center
}
.eyebrow{color:#a78bfa;font-weight:700;letter-spacing:.16em;font-size:11px;text-transform:uppercase}
.workspace{
  border:1px solid var(--border);border-radius:20px;background:var(--panel);
  padding:25px;box-shadow:0 20px 60px rgba(0,0,0,.15)
}
.sidebar-brand{padding:4px 7px 20px;border-bottom:1px solid var(--border);margin-bottom:16px}
.sidebar-brand-title{font-family:"Space Grotesk";font-size:18px;font-weight:700}
.sidebar-brand-copy{color:#737d91;font-size:11px;margin-top:4px}
.footer-note{text-align:center;color:#555e70;font-size:11px;padding:28px 0}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 3. PREMIUM PRODUCT UI COMPONENT SYSTEM
# =============================================================================
st.markdown("""
<style>
.block-container{max-width:1450px!important;padding-top:1.2rem!important}
[data-testid="stAppViewContainer"]{overflow-x:hidden}
::-webkit-scrollbar{width:7px;height:7px}
::-webkit-scrollbar-track{background:#080a10}
::-webkit-scrollbar-thumb{background:#30374a;border-radius:20px}
html,body,[class*="css"]{font-family:"DM Sans",-apple-system,BlinkMacSystemFont,sans-serif}
.fade-up{animation:fadeUp .55s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.glow-line{height:1px;width:100%;margin:22px 0;background:linear-gradient(90deg,transparent,rgba(139,92,246,.55),transparent)}
section[data-testid="stSidebar"]{background:rgba(8,10,17,.97)!important;border-right:1px solid rgba(255,255,255,.07)!important}
section[data-testid="stSidebar"]>div{padding:22px 15px}
section[data-testid="stSidebar"] .stRadio label{border:1px solid transparent;border-radius:12px;padding:9px 11px;transition:.2s}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.08)}
h1,h2,h3{font-family:"Space Grotesk",sans-serif!important;text-transform:none!important;letter-spacing:-.03em!important}
h1{font-size:42px!important}h2{font-size:28px!important}
h3{font-size:12px!important;letter-spacing:.12em!important;color:#a78bfa!important}
button,[data-testid="stButton"] button{border-radius:11px!important;border:1px solid rgba(255,255,255,.1)!important;background:linear-gradient(135deg,#8b5cf6,#6366f1)!important;color:#fff!important;font-weight:700!important;min-height:44px;transition:.18s!important}
button:hover,[data-testid="stButton"] button:hover{transform:translateY(-1px);box-shadow:0 12px 30px rgba(99,102,241,.25)!important}
.stTextInput input,.stTextArea textarea{background:rgba(11,14,23,.92)!important;color:#fff!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;padding:13px 15px!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:rgba(139,92,246,.5)!important;box-shadow:0 0 0 3px rgba(139,92,246,.1)!important}
[data-testid="stChatMessage"]{background:rgba(15,19,29,.76)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:16px!important;padding:16px 18px!important;margin:10px 0!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(20,25,38,.9),rgba(13,16,26,.86));border:1px solid rgba(255,255,255,.08);border-radius:15px;padding:16px}
[data-testid="stMetricLabel"]{color:#8d96aa!important}[data-testid="stMetricValue"]{color:#fff!important;font-family:"Space Grotesk",sans-serif}
div[data-testid="stFileUploader"]{background:rgba(13,17,27,.8);border:1px dashed rgba(139,92,246,.35);border-radius:14px;padding:8px}
.product-topbar{min-height:62px;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:10px 14px 10px 16px;margin-bottom:24px;border:1px solid rgba(255,255,255,.075);border-radius:17px;background:rgba(10,13,21,.78);backdrop-filter:blur(20px);box-shadow:0 14px 45px rgba(0,0,0,.16)}
.product-brand{display:flex;align-items:center;gap:11px}.product-logo{width:36px;height:36px;border-radius:11px;display:grid;place-items:center;background:linear-gradient(135deg,#8b5cf6,#4f46e5);box-shadow:0 8px 28px rgba(99,102,241,.26)}
.product-name{font-family:"Space Grotesk";font-size:15px;font-weight:700;color:#fff}.product-desc{color:#687287;font-size:10px;margin-top:2px}
.top-actions{display:flex;align-items:center;gap:8px}.top-chip{border:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.025);color:#8791a5;border-radius:999px;padding:7px 10px;font-size:10px}.online-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#34d399;box-shadow:0 0 10px #34d399;margin-right:5px}
.dashboard-hero{position:relative;overflow:hidden;padding:48px 42px;border-radius:25px;border:1px solid rgba(255,255,255,.08);background:radial-gradient(circle at 86% 15%,rgba(139,92,246,.23),transparent 26%),radial-gradient(circle at 72% 100%,rgba(59,130,246,.12),transparent 30%),linear-gradient(135deg,rgba(20,25,40,.96),rgba(9,12,20,.96));box-shadow:0 28px 90px rgba(0,0,0,.22)}
.hero-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.22);color:#c4b5fd;font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.hero-title{font-family:"Space Grotesk";font-weight:700;letter-spacing:-.055em;font-size:clamp(43px,6vw,72px);line-height:.98;color:#fff;margin-top:18px}
.hero-gradient{background:linear-gradient(90deg,#fff 10%,#c4b5fd 48%,#60a5fa 90%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-copy{max-width:650px;color:#8993a8;font-size:15px;line-height:1.7;margin-top:16px}.hero-meta{display:flex;flex-wrap:wrap;gap:9px;margin-top:25px}.hero-meta span{border:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.025);border-radius:9px;padding:7px 10px;color:#858fa4;font-size:10px}
.feature-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}.feature-card{min-height:145px;padding:20px;border-radius:17px;border:1px solid rgba(255,255,255,.07);background:linear-gradient(145deg,rgba(18,23,36,.9),rgba(11,14,23,.86));transition:.2s}
.feature-card:hover{transform:translateY(-3px);border-color:rgba(139,92,246,.3);box-shadow:0 16px 45px rgba(0,0,0,.18)}
.feature-icon{width:35px;height:35px;border-radius:10px;display:grid;place-items:center;background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.18);font-size:16px}.feature-title{font-family:"Space Grotesk";font-size:14px;font-weight:700;margin-top:15px;color:#f2f4f9}.feature-copy{color:#707b90;font-size:11px;line-height:1.55;margin-top:5px}
.workspace-header{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin:8px 0 18px}.workspace-kicker{color:#a78bfa;font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}.workspace-title{font-family:"Space Grotesk";font-size:29px;font-weight:700;color:#fff;letter-spacing:-.04em;margin-top:5px}.workspace-copy{color:#747f94;font-size:12px;line-height:1.55;margin-top:5px;max-width:700px}.workspace-badge{border:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.025);color:#8d97aa;border-radius:999px;padding:7px 10px;font-size:9px;white-space:nowrap}
.command-bar{display:flex;align-items:center;gap:10px;padding:11px 13px;margin:14px 0;border:1px solid rgba(255,255,255,.07);border-radius:13px;background:rgba(9,12,19,.75)}.command-key{padding:5px 7px;border-radius:6px;background:#171c28;border:1px solid #252b3a;color:#697489;font-size:9px;font-family:monospace}.command-text{color:#778297;font-size:11px}
.chat-empty{min-height:280px;display:flex;align-items:center;justify-content:center;text-align:center;border:1px dashed rgba(255,255,255,.08);border-radius:18px;background:rgba(8,11,18,.45)}
.editor-head{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border:1px solid rgba(255,255,255,.07);border-bottom:0;border-radius:13px 13px 0 0;background:#0b0e16}.editor-dots{display:flex;gap:5px}.editor-dot{width:7px;height:7px;border-radius:50%;background:#303747}.editor-file{color:#6e788b;font-size:10px;font-family:monospace}
.side-profile{padding:14px;border:1px solid rgba(255,255,255,.07);border-radius:15px;background:linear-gradient(145deg,rgba(25,30,45,.72),rgba(12,15,24,.72));margin-bottom:14px}.side-avatar{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,#8b5cf6,#2563eb);font-family:"Space Grotesk";font-weight:700;color:#fff}.side-name{font-weight:700;color:#f5f7fb;font-size:13px}.side-role{color:#727d91;font-size:10px;margin-top:2px}.side-section{color:#596477;font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;margin:20px 8px 7px}.footer-note{text-align:center;color:#555e70;font-size:10px;padding:28px 0}
@media(max-width:1000px){.feature-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:650px){.feature-grid{grid-template-columns:1fr}.dashboard-hero{padding:32px 22px}.top-chip{display:none}.workspace-header{display:block}}
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
st.markdown("""
<div class="product-topbar fade-up">
  <div class="product-brand">
    <div class="product-logo">✦</div>
    <div><div class="product-name">KUBOOM AI</div><div class="product-desc">Rohit's intelligent workspace</div></div>
  </div>
  <div class="top-actions">
    <div class="top-chip"><span class="online-dot"></span>All systems operational</div>
    <div class="top-chip">Llama powered</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="side-profile">
  <div style="display:flex;align-items:center;gap:10px">
    <div class="side-avatar">R</div>
    <div><div class="side-name">Rohit's Workspace</div><div class="side-role">AI STUDY & CODING ASSISTANT</div></div>
  </div>
</div>
<div class="side-section">Workspace modules</div>
""", unsafe_allow_html=True)
