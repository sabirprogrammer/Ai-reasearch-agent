"""Search tool: lets the agent search the web using DuckDuckGo (free, no API key)."""

from crewai.tools import tool
from ddgs import DDGS


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the internet with DuckDuckGo. Input is a short search query.
    Returns a list of results with title, link and a short summary."""
    try:
        results = DDGS().text(query, max_results=6)
    except Exception as error:  # network problem, rate limit, etc.
        return f"Search failed: {error}. Try a different or shorter query."

    if not results:
        return "No results found. Try a different query."

    lines = []
    for i, r in enumerate(results, start=1):
        lines.append(
            f"{i}. {r.get('title', '')}\n"
            f"   Link: {r.get('href', '')}\n"
            f"   Summary: {r.get('body', '')}"
        )
    return "\n\n".join(lines)
