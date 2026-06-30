"""
app.py — Sports AI Agent
Run: streamlit run app.py
"""

import os
import sys
import time
import datetime
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Make sure tools/ is importable regardless of where streamlit is run from
sys.path.insert(0, os.path.dirname(__file__))
load_dotenv()

st.set_page_config(page_title="NBA AI Agent", page_icon="🏀", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] { background: #0f1117; }
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.tool-badge {
    display: inline-block; background: #1e2847; border: 1px solid #2d3b6e;
    border-radius: 20px; padding: 3px 10px; font-size: 0.76rem;
    color: #7b9cff; margin: 2px 3px;
}
.source-card {
    background: #111827; border-left: 3px solid #3b5bdb;
    border-radius: 6px; padding: 10px 14px; margin: 4px 0;
    font-size: 0.8rem; color: #d1d5db; font-family: monospace;
    white-space: pre-wrap; max-height: 350px; overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for key, val in [("messages", []), ("chat_history", []), ("logs", []), ("n_queries", 0)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏀 NBA AI Agent")
    st.markdown("---")
    groq_key = st.text_input("Groq API Key (optional — faster)", type="password",
                              value=os.getenv("GROQ_API_KEY", ""),
                              help="Free at console.groq.com. If blank, uses local Ollama.")
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.markdown("---")
    st.markdown("### Backend")
    if os.getenv("GROQ_API_KEY"):
        st.success("Groq / Llama 3.3 70B")
    else:
        st.info("Ollama / Llama 3.1 (local)\nMake sure `ollama serve` is running")

    st.markdown("---")
    st.markdown("### Tools")
    st.markdown("""
    🟢 **RAG** ChromaDB rulebook  
    🔵 **LIVE** NBA stats API  
    🔵 **LIVE** Google News  
    🔵 **LIVE** ESPN  
    """)

    st.markdown("---")
    st.metric("Queries", st.session_state.n_queries)
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.n_queries = 0
        st.rerun()

# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown("# 🏀 NBA AI Agent")
st.caption("RAG (ChromaDB rulebook) + Live data (NBA stats, ESPN, Google News)")

chat_tab, logs_tab = st.tabs(["💬 Chat", "📋 Logs"])

EXAMPLES = [
    "What is a flagrant foul and how is it different from a tech foul?",
    "Show how NBA Point Guard scoring evolved from 2015 to 2024",
    "Get current 2024 season stats for the top NBA point guards",
    "What are the shot clock rules?",
    "Find recent news about the NBA MVP race",
    "Compare NBA shooting guard stats over the last 5 seasons",
]

with chat_tab:
    # Show example buttons only when chat is empty
    if not st.session_state.messages:
        st.markdown("### Try one of these:")
        c1, c2 = st.columns(2)
        for i, ex in enumerate(EXAMPLES):
            with (c1 if i % 2 == 0 else c2):
                if st.button(ex[:65] + ("…" if len(ex) > 65 else ""), key=f"ex{i}", use_container_width=True):
                    st.session_state._pending = ex
                    st.rerun()
        st.markdown("---")

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("tools"):
                html = "".join(f'<span class="tool-badge">⚡ {t}</span>' for t in msg["tools"])
                st.markdown(html, unsafe_allow_html=True)
            if msg.get("duration"):
                st.caption(f"⏱ {msg['duration']:.1f}s · {len(msg.get('tools', []))} tools")
            for tool_name, raw in msg.get("raw", {}).items():
                with st.expander(f"📄 Raw: `{tool_name}`"):
                    st.markdown(f'<div class="source-card">{raw}</div>', unsafe_allow_html=True)
            if msg.get("viz_code") and msg.get("raw_text_for_viz"):
                try:
                    import io
                    import plotly.express as px
                    lines = [
                        l for l in msg["raw_text_for_viz"].split("\n")
                        if l.strip() and not any(l.startswith(p)
                        for p in ["NBA", "Source", "─", "Season:"])
                    ]
                    df = pd.read_csv(
                        io.StringIO("\n".join(lines)),
                        sep=r"\s{2,}", engine="python"
                    )
                    df.columns = df.columns.str.strip()
                    _merged = [c for c in df.columns if " " in c.strip()]
                    if _merged:
                        df = df.reset_index()
                        for _m in _merged:
                            _parts = _m.strip().split(None, 1)
                            if len(_parts) == 2:
                                df.rename(columns={"index": _parts[0], _m: _parts[1]}, inplace=True)
                        df.columns = df.columns.str.strip()
                    namespace = {"df": df, "px": px}
                    exec(msg["viz_code"], namespace)
                    fig = namespace.get("fig")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass

    # Input
    user_input = st.chat_input("Ask about NBA rules, stats, or news…")
    if hasattr(st.session_state, "_pending"):
        user_input = st.session_state._pending
        del st.session_state._pending

    if user_input and str(user_input).strip():
        query = str(user_input).strip()
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            t0 = time.time()
            tools_used = []
            raw_outputs = {}

            try:
                from agent import run_query

                with st.status("🔍 Agent working…", expanded=True) as status:
                    st.write("Routing query to tools…")
                    result = run_query(query, chat_history=st.session_state.chat_history)
                    for step in result.get("steps", []):
                        tn = step["tool"]
                        tools_used.append(tn)
                        if step.get("output"):
                            raw_outputs[tn] = step["output"]
                        st.write(f"✅ `{tn}` called")
                    status.update(label="✅ Done", state="complete")

                duration = time.time() - t0
                final = result.get("output", "No response.")
                placeholder.markdown(final)

                if tools_used:
                    html = "".join(f'<span class="tool-badge">⚡ {t}</span>' for t in tools_used)
                    st.markdown(html, unsafe_allow_html=True)
                st.caption(f"⏱ {duration:.1f}s · {len(tools_used)} tools")

                for tn, raw in raw_outputs.items():
                    with st.expander(f"📄 Raw: `{tn}`"):
                        st.markdown(f'<div class="source-card">{raw}</div>', unsafe_allow_html=True)

                _STATS_TOOLS = {
                    "fetch_nba_player_stats", "fetch_nba_team_stats",
                    "fetch_player_advanced_stats", "compare_position_stats_over_seasons",
                    "fetch_league_leaders", "fetch_player_game_log",
                    "fetch_player_career_stats",
                }
                raw_text = None
                for tool_name, raw in raw_outputs.items():
                    if tool_name in _STATS_TOOLS:
                        raw_text = raw
                        break

                if result.get("viz_code") and raw_text:
                    try:
                        import io
                        import plotly.express as px
                        lines = [
                            l for l in raw_text.split("\n")
                            if l.strip()
                            and not any(l.startswith(p) for p in
                                ["NBA", "Source", "─", "Season:", "Seas"])
                        ]
                        df = pd.read_csv(
                            io.StringIO("\n".join(lines)),
                            sep=r"\s{2,}",
                            engine="python",
                        )
                        df.columns = df.columns.str.strip()
                        _merged = [c for c in df.columns if " " in c.strip()]
                        if _merged:
                            df = df.reset_index()
                            for _m in _merged:
                                _parts = _m.strip().split(None, 1)
                                if len(_parts) == 2:
                                    df.rename(columns={"index": _parts[0], _m: _parts[1]}, inplace=True)
                            df.columns = df.columns.str.strip()
                        namespace = {"df": df, "px": px}
                        exec(result["viz_code"], namespace)
                        fig = namespace.get("fig")
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass  # Viz failure never breaks the chat

                st.session_state.messages.append({
                    "role": "assistant", "content": final,
                    "tools": tools_used, "raw": raw_outputs, "duration": duration,
                    "viz_code": result.get("viz_code"),
                    "raw_text_for_viz": raw_text,
                })

                from langchain_core.messages import HumanMessage, AIMessage
                st.session_state.chat_history.extend([
                    HumanMessage(content=query),
                    AIMessage(content=final),
                ])

                st.session_state.logs.append({
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "query": query,
                    "steps": result.get("steps", []),
                    "duration": duration,
                    "answer": final,
                })
                st.session_state.n_queries += 1

            except Exception as e:
                err = f"❌ Error: `{e}`"
                placeholder.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})

with logs_tab:
    if not st.session_state.logs:
        st.info("No queries yet. Ask something in the Chat tab.")
    else:
        for log in reversed(st.session_state.logs):
            with st.expander(f"[{log['time']}] {log['query'][:70]} — {len(log['steps'])} tools · {log['duration']:.1f}s", expanded=False):
                st.markdown(f"**Query:** {log['query']}")
                for i, step in enumerate(log["steps"], 1):
                    st.markdown(f"**Step {i} — `{step['tool']}`**")
                    st.json(step.get("args", {}))
                    if step.get("output"):
                        st.code(step["output"][:1000], language="text")
                st.markdown("**Answer:**")
                st.markdown(log["answer"])
