"""
agent.py
Uses langgraph create_react_agent — works with LangChain 1.x
No AgentExecutor needed.
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

SYSTEM_PROMPT = """You are an expert NBA sports data agent. You have these tools:

- search_vector_db: Search the NBA rulebook stored in ChromaDB. Use this for rules questions.
- fetch_nba_player_stats: Get current season NBA player stats. Use for player performance.
- compare_position_stats_over_seasons: Get multi-season trends. Use for evolution queries.
- search_sports_news: Search Google News for recent NBA articles.
- scrape_espn_headlines: Get ESPN headlines.

Use multiple tools for thorough answers. Always cite sources."""


def get_llm():
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            print("Using Groq / llama-3.3-70b-versatile")
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0,
                api_key=groq_key,
            )
        except Exception as e:
            print(f"WARNING: Groq init failed ({e}), falling back to Ollama / llama3.1")
    else:
        print("WARNING: GROQ_API_KEY not set — falling back to Ollama / llama3.1")

    from langchain_ollama import ChatOllama
    return ChatOllama(model="llama3.1", temperature=0)


def run_query(query: str, chat_history: list = None) -> dict:
    """Run query through the agent. Returns dict with 'output' and 'messages'."""
    from langgraph.prebuilt import create_react_agent
    from tools import get_all_tools

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    llm = get_llm()
    tools = get_all_tools()
    agent = create_react_agent(llm, tools)

    # Build message list with system prompt first
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add chat history if any
    for msg in (chat_history or []):
        messages.append(msg)

    # Add current query
    messages.append(HumanMessage(content=str(query)))

    result = agent.invoke({"messages": messages})

    # Extract final answer — last message in the list
    all_messages = result.get("messages", [])
    final_answer = ""
    for msg in reversed(all_messages):
        if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_call_id"):
            final_answer = msg.content
            break

    # Extract tool calls and their outputs using ID-based matching
    steps = []
    id_to_step = {}
    for msg in all_messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                step = {
                    "tool": tc.get("name", "unknown"),
                    "args": tc.get("args", {}),
                    "output": None,
                }
                steps.append(step)
                tc_id = tc.get("id")
                if tc_id:
                    id_to_step[tc_id] = step
        if hasattr(msg, "tool_call_id") and msg.tool_call_id:
            step = id_to_step.get(msg.tool_call_id)
            if step:
                step["output"] = str(msg.content)[:2000]

    return {
        "output": final_answer,
        "steps": steps,
        "messages": all_messages,
    }
