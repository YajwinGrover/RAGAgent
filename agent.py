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


def build_agent(llm, tools):
    from langgraph.prebuilt import create_react_agent

    from langchain_ollama import ChatOllama
    if isinstance(llm, ChatOllama):
        priority_tools = [
            "search_vector_db",
            "fetch_nba_player_stats",
            "compare_position_stats_over_seasons",
            "fetch_nba_team_stats",
            "fetch_player_career_stats",
            "fetch_league_leaders",
            "search_sports_news",
            "fetch_espn_nba_news",
        ]
        tools = [t for t in tools if t.name in priority_tools]
        print(f"Ollama mode: using {len(tools)} priority tools")

    return create_react_agent(llm, tools)


def generate_visualization(steps: list, llm) -> str | None:
    """
    Looks through tool outputs for tabular stats data.
    If found, asks the LLM to write plotly code for it.
    Returns python code string or None.
    """
    STATS_TOOLS = {
        "fetch_nba_player_stats",
        "fetch_nba_team_stats",
        "fetch_player_advanced_stats",
        "compare_position_stats_over_seasons",
        "fetch_league_leaders",
        "fetch_player_game_log",
        "fetch_player_career_stats",
    }

    tabular_output = None
    for step in steps:
        if step.get("tool") in STATS_TOOLS and step.get("output"):
            tabular_output = step["output"]
            break

    if not tabular_output:
        return None

    # Pre-parse to get the actual column names pandas produces after the merged-header
    # fix, so the LLM references the correct column names in its generated code.
    col_hint = ""
    try:
        import io as _io
        import pandas as _pd
        _skip = ("NBA", "Source", "─", "% Change", "LeBron", "Stephen", "Michael")
        _lines = [l for l in tabular_output.split("\n")
                  if l.strip() and not any(l.startswith(p) for p in _skip)]
        _df = _pd.read_csv(_io.StringIO("\n".join(_lines)), sep=r"\s{2,}", engine="python")
        _df.columns = _df.columns.str.strip()
        # When two headers were only 1 space apart, pandas merges them (e.g.
        # "PLAYER_NAME TEAM_ABBREVIATION") and uses the first data column as index.
        # Reset the index and rename both parts to recover the original columns.
        _merged = [c for c in _df.columns if " " in c.strip()]
        if _merged:
            _df = _df.reset_index()
            for _m in _merged:
                _parts = _m.strip().split(None, 1)
                if len(_parts) == 2:
                    _df.rename(columns={"index": _parts[0], _m: _parts[1]}, inplace=True)
            _df.columns = _df.columns.str.strip()
        col_hint = f"\nIMPORTANT — df already has exactly these column names: {_df.columns.tolist()}"
    except Exception:
        pass

    prompt = f"""You are a data visualization expert.
Given this sports data, write a single Python code block
using plotly.express that creates the most appropriate chart.

Rules:
- The data is already parsed into a pandas DataFrame called df
- Use px.line for trends over time or seasons
- Use px.bar for rankings, top N players, or team comparisons
- Use px.scatter for two-variable player comparisons
- Store the final figure in a variable called fig
- Give it a clear descriptive title
- Label all axes clearly
- Use color where it adds meaning
- Only return the code block, no explanation, no markdown fences
{col_hint}

Data:
{tabular_output[:3000]}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        code = response.content.strip()
        if code.startswith("```"):
            code = "\n".join(code.split("\n")[1:])
        if code.endswith("```"):
            code = "\n".join(code.split("\n")[:-1])
        return code.strip()
    except Exception:
        return None


def run_query(query: str, chat_history: list = None) -> dict:
    """Run query through the agent. Returns dict with 'output' and 'messages'."""
    from tools import get_all_tools

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    llm = get_llm()
    tools = get_all_tools()
    agent = build_agent(llm, tools)

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

    viz_code = generate_visualization(steps, llm)
    return {
        "output": final_answer,
        "steps": steps,
        "messages": all_messages,
        "viz_code": viz_code,
    }
