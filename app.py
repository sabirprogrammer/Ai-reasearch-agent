"""Streamlit user interface for the AI Research Agent."""

import streamlit as st

from research_agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

# ---------- Styling (CSS) ----------
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: linear-gradient(180deg, #eef2ff 0%, #ffffff 45%);}
    .block-container {max-width: 760px; padding-top: 3rem; padding-bottom: 3rem;}

    .hero {text-align: center; margin-bottom: 1.8rem;}
    .hero .badge {
        display: inline-block; padding: 0.25rem 0.9rem; border-radius: 999px;
        background: #e0e7ff; color: #4338ca; font-size: 0.8rem; font-weight: 600;
        letter-spacing: 0.04em; margin-bottom: 0.9rem;
    }
    .hero h1 {
        font-size: 2.8rem; font-weight: 800; margin: 0; padding: 0;
        background: linear-gradient(90deg, #4f46e5, #9333ea);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p {color: #64748b; font-size: 1.05rem; margin-top: 0.6rem;}

    /* input box */
    div[data-baseweb="input"] {border-radius: 14px; border: 1px solid #c7d2fe; background: #ffffff;}
    div[data-baseweb="input"] input {padding: 0.8rem 1rem; font-size: 1.05rem;}

    /* buttons */
    div.stButton > button {
        border-radius: 12px; font-weight: 600; padding: 0.6rem 1rem;
        border: 1px solid #c7d2fe; background: #ffffff; color: #4338ca;
    }
    div.stButton > button:hover {border-color: #4f46e5; color: #4f46e5;}
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4f46e5, #9333ea); color: #ffffff; border: none;
        padding: 0.8rem 1rem; font-size: 1.05rem;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.30);
    }
    div.stButton > button[kind="primary"]:hover {color: #ffffff; opacity: 0.92;}

    /* report card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px; background: #ffffff; border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }
    .small-note {text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 2.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <span class="badge">POWERED BY CREWAI</span>
        <h1>AI Research Agent</h1>
        <p>Give me any topic. I will search the web and write a clear report for you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- API key (ONLY from Streamlit Secrets) ----------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error('GROQ_API_KEY not found. Add it in Settings → Secrets:  GROQ_API_KEY = "your_key"')
    st.stop()

# ---------- Input ----------
EXAMPLES = ["Future of electric cars", "Benefits of intermittent fasting", "How does quantum computing work"]


def use_example(text: str) -> None:
    st.session_state["topic"] = text


topic = st.text_input(
    "Topic", key="topic", placeholder="🔎  What do you want to research?", label_visibility="collapsed"
)

cols = st.columns(len(EXAMPLES))
for col, example in zip(cols, EXAMPLES):
    col.button(example, key=f"ex_{example}", on_click=use_example, args=(example,), use_container_width=True)

st.write("")
generate = st.button("✨ Generate Report", type="primary", use_container_width=True)

# ---------- Run the agent ----------
if generate:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.status("Agent is working: searching the web and writing your report...", expanded=False) as status:
            try:
                st.session_state["report"] = run_research(topic.strip(), api_key)
                st.session_state["report_topic"] = topic.strip()
                status.update(label="Report is ready!", state="complete")
            except Exception as error:
                status.update(label="Something went wrong", state="error")
                st.error(f"Error: {error}")

# ---------- Show the report ----------
if "report" in st.session_state:
    st.write("")
    with st.container(border=True):
        st.caption(f"📄 REPORT  ·  {st.session_state.get('report_topic', '')}")
        st.markdown(st.session_state["report"])
    st.write("")
    st.download_button(
        "⬇️ Download report",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.markdown('<p class="small-note">Built with CrewAI · Groq · Streamlit</p>', unsafe_allow_html=True)
