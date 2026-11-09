"""Streamlit user interface for the AI Research Agent."""

import streamlit as st

from research_agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

# Small bit of styling: hide Streamlit's default menu/footer for a clean look
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {max-width: 720px; padding-top: 4rem;}
    h1 {text-align: center; font-weight: 700;}
    .subtitle {text-align: center; color: #888; margin-bottom: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Research Agent")
st.markdown('<p class="subtitle">Type a topic and get a research report.</p>', unsafe_allow_html=True)

# The API key comes ONLY from Streamlit Secrets (App -> Settings -> Secrets)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error('GROQ_API_KEY not found. Add it in Settings → Secrets:  GROQ_API_KEY = "your_key"')
    st.stop()

topic = st.text_input("Topic", placeholder="e.g. Future of electric cars", label_visibility="collapsed")

if st.button("Generate Report", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Researching... this can take up to a minute"):
            try:
                st.session_state["report"] = run_research(topic.strip(), api_key)
            except Exception as error:
                st.error(f"Something went wrong: {error}")

if "report" in st.session_state:
    st.divider()
    st.markdown(st.session_state["report"])
    st.download_button(
        "Download report",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
