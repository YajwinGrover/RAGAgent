"""
agent.py
────────
LangChain tool-calling agent powered by Groq (free tier).

The agent:
  1. Reads the user query
    2. Decides which tools to call (basketball-ref, news, ESPN)
  3. Calls them, collects raw data
  4. Returns a structured summary WITH all sourced data attached

Using Groq because:
  - Free tier with generous rate limits
  - Extremely fast (token generation in milliseconds)
  - Supports tool calling with llama-3.3-70b-versatile
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from tools import get_all_tools

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# System prompt — tells the agent its ONLY job today is to source data
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert sports data sourcing agent. Your ONLY job today is to 
COLLECT and PRESENT raw data from multiple reliable sources. You are the data pipeline — 
not the analyst.

WHEN given a query:
1. Break down what data needs to be sourced (stats, articles, headlines)
2. Call the appropriate tools — use MULTIPLE tools for a thorough data collection
3. Present ALL collected data clearly, organized by source
4. ALWAYS cite where each piece of data came from (URL, outlet/source name)
5. DO NOT editorialize, rank, or analyze — just gather and present the raw data

TOOL SELECTION GUIDE:
- "evolution", "trend", "over time", "history" → use compare_position_stats_over_seasons first
- "current season", "this year", "2024" → use fetch_nba_player_stats
 
- "news", "recent", "latest" → use search_sports_news
- "ESPN", "headlines" → use scrape_espn_headlines

FORMAT your output as:
📊 STATISTICAL DATA (from Basketball Reference)
[tables here]

📰 NEWS COVERAGE
[articles here]

 

Be THOROUGH. A query about "PG evolution" should pull multi-season trend data,
current top PGs, relevant news, and community discussion — all of it.
"""

# ─────────────────────────────────────────────────────────────────────────────
# Agent factory
# ─────────────────────────────────────────────────────────────────────────────

def build_agent(model: str = "llama-3.3-70b-versatile"):
    """
    Build and return a configured LangChain AgentExecutor.

    Args:
        model: Groq model to use. Recommended:
               'llama-3.3-70b-versatile'  — best quality, great tool calling
               'llama-3.1-8b-instant'     — fastest, lighter queries

    Returns:
        An AgentExecutor ready to handle queries.
    """
    llm = ChatGroq(
        model=model,
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    tools = get_all_tools()

    # The installed LangChain exposes `create_agent(...)` which returns a
    # compiled agent graph. We pass the chat model instance and tools directly
    # and supply the system prompt via `system_prompt` so the model receives it.
    agent_graph = create_agent(
        llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        debug=False,
        name="rag_agent",
    )

    return agent_graph


# ─────────────────────────────────────────────────────────────────────────────
# Convenience wrapper used by app.py
# ─────────────────────────────────────────────────────────────────────────────

def run_query(
    query: str,
    chat_history: list | None = None,
    model: str = "llama-3.3-70b-versatile",
) -> dict:
    """
    Run a query through the agent and return the full result dict.

    Returns dict with keys:
        'output'              — final answer string
        'intermediate_steps'  — list of (AgentAction, tool_output) tuples
    """
    # Validate input early to avoid passing None to LLM/message constructors
    if not query or not isinstance(query, str):
        raise ValueError(f"Query must be a non-empty string, got: {type(query)}")

    agent = build_agent(model=model)
    history = chat_history or []

    # The compiled agent accepts an invocation dict; middleware/examples in
    # the installed LangChain call `agent.invoke({"messages": [HumanMessage(...) ]})`
    messages = [HumanMessage(query)]
    if history:
        # If caller passed chat history as a list of strings, append them as prior human messages
        for h in history:
            messages.insert(0, HumanMessage(h))

    result = agent.invoke({"messages": messages})

    return result
