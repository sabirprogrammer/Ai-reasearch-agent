# 🔎 AI Research Agent (CrewAI + Groq + Streamlit)

Type a topic → one AI agent searches the web with DuckDuckGo → writes a Markdown report.

## Files
| File | What it does |
|---|---|
| `app.py` | The Streamlit web page (input box, button, report) |
| `research_agent.py` | The CrewAI agent, task and crew |
| `tools.py` | The DuckDuckGo search tool |
| `requirements.txt` | Libraries (exact versions that work together) |
| `.streamlit/secrets.toml.example` | Example of how to write your API key in Streamlit Secrets |

## Deploy on Streamlit Cloud
1. Upload all these files to a GitHub repository.
2. Go to https://share.streamlit.io → **Create app** → pick your repo, branch `main`, main file `app.py`.
3. Open **Advanced settings** → choose **Python 3.12** → paste in **Secrets**:
   ```toml
   GROQ_API_KEY = "your_real_key"
   ```
   (Get a key at https://console.groq.com/keys)
4. Click **Deploy**.
