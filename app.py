import json
import streamlit as st

from agents.orchestrator import Orchestrator
from agent_os.snapshot import parse_snapshot

st.set_page_config(
    page_title="Binance Risk Sentinel",
    page_icon="🛡️",
    layout="wide",
)

st.markdown("""
<style>
    .stApp { background: #0b0e11; color: #eaecef; }
    .block-container { padding-top: 1.5rem; max-width: 1400px; }
    .hero {
        padding: 1.2rem 1.4rem;
        border: 1px solid #2b3139;
        border-radius: 14px;
        background: linear-gradient(135deg,#11161d,#0d1117);
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 2.1rem; }
    .hero p { color: #a7b1bb; margin: .35rem 0 0; }
    .metric {
        border: 1px solid #2b3139; border-radius: 12px;
        padding: 1rem; background: #11161d;
    }
    .metric .label { color: #848e9c; font-size: .85rem; }
    .metric .value { font-size: 1.55rem; font-weight: 700; margin-top: .2rem; }
    .trace {
        border-left: 3px solid #f0b90b; padding: .65rem .9rem;
        background: #11161d; margin: .45rem 0; border-radius: 0 8px 8px 0;
    }
    .warn {
        padding: .8rem 1rem; border-radius: 10px;
        background: #241d0a; border: 1px solid #5c4810;
    }
    .safe {
        padding: .8rem 1rem; border-radius: 10px;
        background: #0e2118; border: 1px solid #194d31;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🛡️ Binance Risk Sentinel</h1>
  <p>Explainable Multi-Agent Risk Control System for Binance Agent OS</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Control Panel")
    symbol = st.selectbox("Market", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"])
    risk_budget = st.slider("Risk budget (%)", 0.25, 5.0, 1.0, 0.25)
    demo_mode = st.toggle("Demo mode", value=True)
    st.divider()
    st.caption("Execution policy")
    st.write("🟢 Analysis is allowed")
    st.write("🟡 Proposal requires review")
    st.write("🔴 Execution requires explicit confirmation")
    st.divider()
    st.caption("Agent OS MCP endpoint")
    st.code("https://agent.binance.com/mcp/agentic", language="text")

    st.subheader("Optional MCP snapshot")
    snapshot_text = st.text_area(
        "Paste JSON returned by your Agent OS-compatible client",
        height=150,
        placeholder='{"balances":[...],"positions":[...]}'
    )

snapshot = parse_snapshot(snapshot_text) if snapshot_text.strip() else None

if st.button("Run Sentinel Scan", type="primary", use_container_width=True):
    with st.spinner("Running Market → Risk → Portfolio → Decision agents..."):
        result = Orchestrator().run(
            symbol=symbol,
            risk_budget_pct=risk_budget,
            demo_mode=demo_mode,
            snapshot=snapshot,
        )
    st.session_state["result"] = result

result = st.session_state.get("result")

if not result:
    st.info("Choose a market and run the Sentinel Scan. Demo mode works without API credentials.")
    st.stop()

market = result.market
risk = result.risk
portfolio = result.portfolio
decision = result.decision

cols = st.columns(5)
metrics = [
    ("Market regime", market["regime"]),
    ("24h change", f'{market["change_pct"]:.2f}%'),
    ("Volatility proxy", f'{market["range_pct"]:.2f}%'),
    ("Risk score", f'{risk["score"]}/100'),
    ("Decision", decision["action"]),
]
for col, (label, value) in zip(cols, metrics):
    col.markdown(
        f'<div class="metric"><div class="label">{label}</div>'
        f'<div class="value">{value}</div></div>',
        unsafe_allow_html=True
    )

st.divider()
left, right = st.columns([1.15, 1])

with left:
    st.subheader("Agent reasoning trace")
    for step in result.trace:
        st.markdown(
            f'<div class="trace"><b>{step["agent"]}</b> — {step["message"]}</div>',
            unsafe_allow_html=True
        )

    st.subheader("Decision")
    st.markdown(f"**Recommendation:** `{decision['action']}`")
    st.write(decision["summary"])
    st.write("**Why:**", decision["why"])
    st.write("**Invalidation:**", decision["invalidation"])

with right:
    st.subheader("Risk controls")
    st.write(f"**Portfolio risk state:** {portfolio['state']}")
    st.write(f"**Suggested max notional:** {risk['max_notional_pct']:.2f}% of available capital")
    st.write(f"**Position sizing factor:** {risk['size_factor']:.2f}×")
    st.write(f"**Risk budget:** {risk_budget:.2f}%")
    st.write("")
    st.markdown(
        '<div class="warn"><b>Human confirmation boundary</b><br>'
        'The Sentinel does not place an order from this dashboard. '
        'A real execution must be explicitly confirmed in the Agent OS-compatible client.</div>',
        unsafe_allow_html=True
    )

st.subheader("Structured proposal")
st.json({
    "symbol": symbol,
    "action": decision["action"],
    "entry_logic": decision["entry_logic"],
    "stop_logic": decision["stop_logic"],
    "risk_budget_pct": risk_budget,
    "max_notional_pct": risk["max_notional_pct"],
    "confidence": decision["confidence"],
    "execution": "BLOCKED_UNTIL_HUMAN_CONFIRMATION",
})

with st.expander("Raw multi-agent state"):
    st.json(result.to_dict())

st.caption("Educational software. Not investment advice. Demo mode uses synthetic portfolio state and Binance public market data.")
