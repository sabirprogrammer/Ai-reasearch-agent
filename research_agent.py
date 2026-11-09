"""The CrewAI part: ONE agent + ONE task that researches a topic and writes a report."""

import os

# Turn off anonymous telemetry (keeps the app quiet and faster to start)
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai import Agent, Crew, LLM, Process, Task  # noqa: E402

from tools import web_search  # noqa: E402

# Groq speaks the "OpenAI-compatible" language, so we use CrewAI's OpenAI connector
# and point it at Groq's address. The first "openai/" selects the connector;
# the rest ("openai/gpt-oss-120b") is the real model name on Groq.
MODEL_NAME = "openai/openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

MAX_TRIES = 3  # the model sometimes makes a mistake; we simply try again


def _run_once(topic: str, api_key: str, strict: bool) -> str:
    """Build the agent, task and crew, run them once, and return the report text."""

    # 1) The brain: the LLM served by Groq
    llm = LLM(model=MODEL_NAME, api_key=api_key, base_url=GROQ_BASE_URL, temperature=0.2)

    # 2) The agent: a researcher that can use the search tool
    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research the topic '{topic}' thoroughly and write a clear, accurate report.",
        backstory=(
            "You are an expert researcher. You search the web, compare sources, "
            "and write well-organised reports. You never invent facts or links. "
            "You have exactly ONE tool: 'Web Search'. No other tool exists, so you never "
            "try to open links, files or web pages. You work only from the search results."
        ),
        tools=[web_search],
        llm=llm,
        max_iter=8,        # max thinking/search steps (prevents endless loops)
        verbose=False,
        allow_delegation=False,
    )

    extra = (
        "\nIMPORTANT: Only call the tool named 'Web Search'. Never call any other tool "
        "(for example open_file or browser). Do not open links."
        if strict
        else ""
    )

    # 3) The task: what we want the agent to do
    task = Task(
        description=(
            f"Research the topic: {topic}\n\n"
            "Use the Web Search tool 2-4 times with different queries. "
            "The search results already contain a title, link and summary: use those. "
            "Then write a report based only on what you found." + extra
        ),
        expected_output=(
            "A report in Markdown with these sections:\n"
            "# Title\n"
            "## Summary (3-4 sentences)\n"
            "## Key Findings (bullet points)\n"
            "## Detailed Analysis (a few paragraphs)\n"
            "## Conclusion\n"
            "## Sources (list of the links you used)"
        ),
        agent=researcher,
    )

    # 4) The crew: runs the task with the agent
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    return crew.kickoff().raw  # the final report text


def run_research(topic: str, api_key: str) -> str:
    """Research `topic` on the web and return a Markdown report (as text)."""
    last_error = None
    for attempt in range(MAX_TRIES):
        try:
            return _run_once(topic, api_key, strict=attempt > 0)
        except Exception as error:
            last_error = error
            text = str(error)
            # Retry only for the model's "wrong tool" mistake or short rate-limit hiccups
            if "tool_use_failed" in text or "Tool call validation" in text or "429" in text:
                continue
            raise
    raise last_error
