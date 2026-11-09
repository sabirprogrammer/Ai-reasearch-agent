"""Streamlit user interface for the AI Research Agent."""

import streamlit as st

from research_agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")
st.title("🔎 AI Research Agent")
st.caption("Enter a topic. The agent searches the web (DuckDuckGo) and writes a report.")

# The API key comes ONLY from Streamlit Secrets (App -> Settings -> Secrets)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error(
        "GROQ_API_KEY not found. In Streamlit Cloud open your app → Settings → Secrets "
        'and add:  GROQ_API_KEY = "your_key"'
    )
    st.stop()

topic = st.text_input("Research topic", placeholder="e.g. Future of electric cars in Pakistan")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Researching... this can take 30-90 seconds"):
            try:
                st.session_state["report"] = run_research(topic.strip(), api_key)
            except Exception as error:
                st.error(f"Something went wrong: {error}")

if "report" in st.session_state:
    st.divider()
    st.markdown(st.session_state["report"])
    st.download_button(
        "Download report (.md)",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
