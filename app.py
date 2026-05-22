"""
app.py
──────
Streamlit frontend for the Sports AI Data Sourcing Agent.

Run with:
    streamlit run app.py
"""

import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Page config — must be FIRST Streamlit call
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Sports AI Agent",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS — makes the app look polished
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}

section[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ── Main header ── */
.main-header {
    background: linear-gradient(135deg, #1a1f35 0%, #0d1b2a 100%);
    border: 1px solid #2d3555;
    border-radius: 14px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.main-header h1 {
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.main-header p {
    color: #8892b0;
    margin: 4px 0 0 0;
    font-size: 0.9rem;
}

/* ── Tool call badge ── */
.tool-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1e2847;
    border: 1px solid #2d3b6e;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #7b9cff;
    font-weight: 500;
    margin: 3px 4px;
}

.tool-call-row {
    margin: 8px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
}

.tool-call-label {
    font-size: 0.78rem;
    color: #6b7280;
    margin-right: 4px;
}

/* ── Source cards ── */
.source-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 3px solid #3b5bdb;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 0.82rem;
    color: #d1d5db;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    overflow-x: auto;
    max-height: 400px;
    overflow-y: auto;
}

/* ── Suggestion chips ── */
.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 16px 0;
}

.suggestion-chip {
    background: #1a1f35;
    border: 1px solid #2d3555;
    border-radius: 10px;
    padding: 12px 16px;
    color: #a0aec0;
    font-size: 0.84rem;
    cursor: pointer;
    transition: all 0.2s;
}

.suggestion-chip:hover {
    background: #1e2847;
    border-color: #3b5bdb;
    color: #ffffff;
}

/* ── Status pills ── */
.status-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-live { background: #14532d; color: #4ade80; }
.status-error { background: #450a0a; color: #f87171; }

/* ── Chat message tweaks ── */
.stChatMessage {
    border-radius: 12px !important;
    padding: 4px 0 !important;
}

/* ── Divider ── */
hr { border-color: #1e2130 !important; }

/* ── Expander styling ── */
.streamlit-expanderHeader {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 8px !important;
    color: #9ca3af !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session state initialisation
# ─────────────────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏀 Sports AI Agent")
    st.markdown("---")

    st.markdown("### 🔑 API Keys")

    groq_key = st.text_input(
        "Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="Free at console.groq.com — no credit card needed",
    )
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    # ... Reddit inputs removed per project configuration (no Reddit integration)

    st.markdown("---")
    st.markdown("### ⚙️ Model")

    model_choice = st.selectbox(
        "Groq Model",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ],
        index=0,
        help="70b = best quality | 8b = fastest",
    )

    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    use_bball_ref = st.checkbox("Basketball Reference", value=True)
    use_news = st.checkbox("Google News", value=True)
    use_espn = st.checkbox("ESPN Headlines", value=True)

    st.markdown("---")
    st.markdown(f"### 📈 Session Stats")
    st.metric("Queries Run", st.session_state.total_queries)

    if st.button("🗑  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.total_queries = 0
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#4b5563;'>
    <b>Free Tier Limits</b><br>
    Groq: ~30 req/min<br>
    Google News: unlimited<br>
    Bball-Ref: be polite (2s delay built in)
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="main-header">
    <div style="font-size:2.5rem;">🏀</div>
    <div>
        <h1>Sports AI Data Agent</h1>
        <p>Sources raw statistics, news, and community discussion across the web</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Ensure agent_logs exists in session_state
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []


# ── API key warning ──
if not os.getenv("GROQ_API_KEY"):
    st.warning(
        "⚠️  **No Groq API key found.** Add it in the sidebar or create a `.env` file. "
        "Get a free key at [console.groq.com](https://console.groq.com).",
        icon="🔑",
    )

# ─────────────────────────────────────────────────────────────────────────────
# Suggested queries (shown only when chat is empty)
# ─────────────────────────────────────────────────────────────────────────────

EXAMPLE_QUERIES = [
    "Show me how NBA Point Guard scoring has evolved from 2015 to 2024, focusing on stats beyond passing",
    "Get me current 2024 season stats for the top NBA centers — scoring, rebounding, and blocks",
    "Find discussions and news about whether Luka Doncic is the best PG in the league right now",
    "Compare NBA shooting guard offensive stats across the last 5 seasons — points, 3-point shooting, efficiency",
    "Source the latest news and community discussion around the 2024 NBA MVP race",
    "Get me advanced stats for all NBA small forwards this season — PER, WS, BPM, VORP",
]

if not st.session_state.messages:
    st.markdown("### 💡 Example queries to get started")
    cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_QUERIES):
        with cols[i % 2]:
            if st.button(f"🔍 {example[:65]}…" if len(example) > 65 else f"🔍 {example}",
                         key=f"example_{i}",
                         use_container_width=True):
                if example and isinstance(example, str):
                    st.session_state._pending_query = example
                    st.rerun()

    st.markdown("---")

# Tabs: Chat + Agent Logs
chat_tab, logs_tab = st.tabs(["Chat", "Agent Logs"])

with chat_tab:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show tool call badges if recorded
            if message.get("tools_used"):
                badge_html = '<div class="tool-call-row"><span class="tool-call-label">🔧 Tools used:</span>'
                for tool_name in message["tools_used"]:
                    badge_html += f'<span class="tool-badge">⚡ {tool_name}</span>'
                badge_html += "</div>"
                st.markdown(badge_html, unsafe_allow_html=True)

            # Show raw tool outputs in expanders
            if message.get("raw_outputs"):
                for tool_name, raw_output in message["raw_outputs"].items():
                    with st.expander(f"📄 Raw data from `{tool_name}`", expanded=False):
                        st.markdown(f'<div class="source-card">{raw_output}</div>',
                                    unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # Chat input — handle pending query from button clicks OR typed input
    # ─────────────────────────────────────────────────────────────────────────────

    user_input = st.chat_input("Ask the agent to source sports data… e.g. 'NBA PG scoring evolution 2015-2024'")
    # Strict guard: only accept non-empty strings
    if not (user_input and isinstance(user_input, str) and user_input.strip()):
        user_input = None

    # Check for a pending query from example button click
    if hasattr(st.session_state, "_pending_query"):
        user_input = st.session_state._pending_query
        del st.session_state._pending_query

    # Process the query (same logic as before)
    if user_input and user_input.strip():

        # Guard — need Groq key
        if not os.getenv("GROQ_API_KEY"):
            st.error("Add your Groq API key in the sidebar first.")
            st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
            st.markdown(user_input)

    # Run the agent
    with st.chat_message("assistant"):
            status_placeholder = st.empty()
            response_placeholder = st.empty()

            tools_used = []
            raw_outputs = {}

            try:
                # Import agent here so it picks up any env vars set in sidebar
                from agent import run_query

                with st.status("🔍 Agent sourcing data…", expanded=True) as status_box:
                    st.write("📡 Identifying relevant data sources…")
                    time.sleep(0.3)

                    # Final guard before calling run_query
                    query = user_input
                    if not query or not isinstance(query, str) or not query.strip():
                        st.error("Query cannot be empty")
                        st.stop()

                    start_ts = time.time()
                    result = run_query(
                        query=query,
                        chat_history=st.session_state.chat_history,
                        model=model_choice,
                    )
                    elapsed = time.time() - start_ts

                    # Extract intermediate steps (tool calls + outputs)
                    step_list = []
                    for action, output in result.get("intermediate_steps", []):
                        tool_name = getattr(action, "tool", str(action))
                        tool_args = getattr(action, "tool_input", {})
                        tools_used.append(tool_name)
                        raw_outputs[tool_name] = str(output)
                        st.write(f"✅ Called `{tool_name}` with args: `{tool_args}`")
                        step_list.append({
                            "tool": tool_name,
                            "args": tool_args,
                            "output": str(output),
                        })

                    status_box.update(label="✅ Data sourced successfully!", state="complete")

                final_answer = result.get("output", "No response generated.")

                # Display final answer with small indicator for tools/time
                response_placeholder.markdown(final_answer)
                if tools_used:
                    st.markdown(f"<div style='font-size:0.8rem;color:#6b7280;margin-top:6px;'>Tools used: {len(tools_used)} • Elapsed: {elapsed:.1f}s</div>", unsafe_allow_html=True)

                # Show tool badge row
                if tools_used:
                    badge_html = '<div class="tool-call-row"><span class="tool-call-label">🔧 Tools used:</span>'
                    for t in tools_used:
                        badge_html += f'<span class="tool-badge">⚡ {t}</span>'
                    badge_html += "</div>"
                    st.markdown(badge_html, unsafe_allow_html=True)

                # Show raw data expanders
                if raw_outputs:
                    for t_name, raw in raw_outputs.items():
                        with st.expander(f"📄 Raw data from `{t_name}`", expanded=False):
                            st.markdown(f'<div class="source-card">{raw}</div>',
                                        unsafe_allow_html=True)

                # Save to session state (messages) and agent_logs
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_answer,
                    "tools_used": tools_used,
                    "raw_outputs": raw_outputs,
                })

                # Append to agent_logs
                log_entry = {
                    "timestamp": time.time(),
                    "query": user_input,
                    "steps": step_list,
                    "iteration_count": len(result.get("intermediate_steps", [])),
                    "tool_count": len(tools_used),
                    "elapsed": elapsed,
                }
                st.session_state.agent_logs.append(log_entry)

                # Update LangChain chat history for multi-turn memory
                st.session_state.chat_history.extend([
                    HumanMessage(content=str(user_input)),
                    AIMessage(content=str(final_answer)),
                ])

                st.session_state.total_queries += 1

            except Exception as exc:
                error_msg = f"❌ **Agent error:** `{exc}`\n\nCheck your API keys and try again."
                response_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                })

with logs_tab:
    st.header("Agent Logs & Raw Data")

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Clear Logs"):
            st.session_state.agent_logs = []
            st.success("Logs cleared")

    # Display logs
    if not st.session_state.agent_logs:
        st.info("No agent logs yet. Run a query from the Chat tab to populate logs.")
    else:
        for entry in reversed(st.session_state.agent_logs[-50:]):
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp']))
            with st.expander(f"{ts} — {entry['query']}", expanded=False):
                st.markdown(f"**Iteration count:** {entry.get('iteration_count',0)}  •  **Tools called:** {entry.get('tool_count',0)}  •  **Elapsed:** {entry.get('elapsed',0):.1f}s")
                for step in entry.get('steps', []):
                    st.markdown(f"**Tool:** `{step['tool']}` — args: `{step['args']}`")
                    st.code(step['output'], language='')

    st.markdown("---")

    # Raw Data Explorer — show most recent tool outputs as dataframes where possible
    st.subheader("Raw Data Explorer")
    # Collect latest outputs
    latest_outputs = {}
    if st.session_state.agent_logs:
        latest = st.session_state.agent_logs[-1]
        for s in latest.get('steps', []):
            latest_outputs[s['tool']] = s['output']

    if not latest_outputs:
        st.info("No raw tool outputs available yet.")
    else:
        for tool_name, raw in latest_outputs.items():
            st.markdown(f"### {tool_name}")
            # Try to parse CSV/TSV-ish or tabular data
            import io
            import pandas as pd
            parsed = None
            try:
                # Try CSV
                parsed = pd.read_csv(io.StringIO(raw))
            except Exception:
                try:
                    parsed = pd.read_table(io.StringIO(raw))
                except Exception:
                    parsed = None

            if parsed is not None and not parsed.empty:
                st.dataframe(parsed)
            else:
                st.code(raw, language='')

# End of file — chat input handled inside the Chat tab above
