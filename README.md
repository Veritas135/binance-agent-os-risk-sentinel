# Binance Risk Sentinel

**An Explainable Multi-Agent Risk Control System for Binance Agent OS**

Binance Risk Sentinel is a Track A-style Agent OS project focused on one question:

> **Before an AI agent trades, can it explain the market, quantify risk, inspect portfolio exposure, and stop for human approval?**

Instead of building another black-box "AI trader", Sentinel decomposes the workflow into four specialized agents:

- **Market Agent** — market regime, momentum and volatility proxy
- **Risk Agent** — risk score, sizing factor and maximum proposed notional
- **Portfolio Agent** — account exposure/state from an Agent OS snapshot when available
- **Decision Agent** — converts the combined state into an explainable action

The system deliberately stops at a **human confirmation boundary** before execution.

---

## Why this project

Agentic trading is not only about generating an order. A useful agent should be able to answer:

1. What is happening in the market?
2. How risky is the current setup?
3. What is already in the portfolio?
4. What exactly is the agent proposing?
5. What would invalidate the proposal?
6. Has a human explicitly authorized execution?

Sentinel makes those steps visible in a compact dashboard and maps the account-aware path to Binance Agent OS / MCP.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    ORCHESTRATOR      │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             ▼                      ▼                      ▼
     ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
     │ Market Agent │       │  Risk Agent   │       │ Portfolio    │
     │              │       │              │       │ Agent        │
     └──────┬───────┘       └──────┬───────┘       └──────┬───────┘
            └──────────────────────┼──────────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │   Decision Agent     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ HUMAN CONFIRMATION   │
                         │       REQUIRED       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Binance Agent OS /   │
                         │ MCP-compatible client│
                         └──────────────────────┘
```

---

## Repository structure

```text
.
├── app.py
├── agents/
│   ├── base.py
│   ├── market_agent.py
│   ├── risk_agent.py
│   ├── portfolio_agent.py
│   ├── decision_agent.py
│   └── orchestrator.py
├── agent_os/
│   ├── MCP_SETUP.md
│   ├── snapshot.py
│   └── system_prompt.md
├── data/
│   └── binance_public.py
├── requirements.txt
├── SUBMISSION_CHECKLIST.md
└── DEMO_SCRIPT.md
```

---

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start:

```bash
streamlit run app.py
```

The dashboard works in demo mode without Binance credentials.

---

## Live public market data

Turn off Demo mode to query Binance's public 24h ticker endpoint.

This path does **not** require account credentials.

The app calculates:

- 24h percentage change
- high-low range percentage
- a simple market regime
- a deterministic risk score
- a sizing constraint

This is deliberately transparent so the demo can be audited.

---

## Agent OS / MCP integration

The account-aware production path is designed around Binance Agent OS / MCP.

Official endpoint:

```text
https://agent.binance.com/mcp/agentic
```

The repository does not store API keys, session tokens, or private credentials.

Instead, authentication and permission control stay inside the Agent OS-compatible client.

See:

- `agent_os/MCP_SETUP.md`
- `agent_os/system_prompt.md`

The Streamlit app can also accept a JSON account snapshot exported/pasted from an authenticated Agent OS-compatible session. This allows the Portfolio Agent to reason about actual positions without embedding credentials in the dashboard.

---

## Security model

Sentinel follows a simple principle:

> **Analysis can be automated; authorization cannot.**

The project therefore separates:

**Read / Analyze**

- market context
- balances/positions when supplied through Agent OS
- risk calculations
- decision proposal

from:

**Act**

- order placement or other supported account actions

The dashboard does not place orders.

A real execution should happen only after explicit human confirmation in the authenticated Agent OS-compatible environment.

No withdrawal workflow is implemented.

---

## Example

Input:

```text
Market: BTCUSDT
Risk budget: 1%
Portfolio: FLAT
```

Possible output:

```text
Market regime: BULLISH_MOMENTUM
Risk score: 48/100
Decision: WATCH_LONG
Confidence: 0.70

Why:
Momentum is positive, but the current state is not enough to justify
an immediate execution.

Invalidation:
The proposal becomes invalid if the market regime flips or risk
increases materially.

Execution:
BLOCKED_UNTIL_HUMAN_CONFIRMATION
```

The important point is not the particular signal. It is the **decision chain**.

---

## Hackathon demo flow

A clean 60–90 second demo:

1. Open the Sentinel dashboard.
2. Select BTCUSDT.
3. Run the scan.
4. Show the four-agent reasoning trace.
5. Change the risk budget and run again.
6. Show how the risk agent changes the proposed notional.
7. Paste an example Agent OS account snapshot.
8. Show Portfolio Agent changing from `FLAT` to `EXPOSED`.
9. Show the Decision Agent adapting the proposal.
10. End on the red/amber **Human Confirmation** boundary.
11. Switch to your Agent OS-compatible client and show the Binance MCP connection separately if available.

This tells a much stronger story than a UI that simply prints a random "BUY" signal.

---

## Important implementation note

The Streamlit application is a reproducible demonstration layer.

It does **not** pretend that a normal Streamlit HTTP request is itself the Binance Agent OS MCP authentication layer.

The real Agent OS integration belongs in the supported AI-agent client, where Binance MCP permissions are configured and controlled.

That separation is intentional.

---

## Open-source project files

This repository includes:

- `CONTRIBUTING.md` — development and pull-request guidance
- `SECURITY.md` — credential and vulnerability handling policy
- `CODE_OF_CONDUCT.md` — community expectations
- `CHANGELOG.md` — release history
- `docs/ARCHITECTURE.md` — system design and trust boundaries
- `.github/workflows/ci.yml` — automated Python 3.10–3.12 tests
- `.github/ISSUE_TEMPLATE/` — structured bug and feature reports
- `GITHUB_PUBLISH.md` — exact GitHub publishing steps

The current release is **v0.2.0**.

---

## Disclaimer

This is an educational hackathon project, not investment advice.

Market regimes and risk scores are simplified demonstration logic. They are not a validated trading strategy and should not be used as the sole basis for financial decisions.

---

## License

MIT

---

## Real MCP demo path

For a real Binance Agent OS demonstration, see [`REAL_MCP_DEMO.md`](REAL_MCP_DEMO.md).

The public repository includes only a **sanitized fictional snapshot** at
`data/example_mcp_snapshot.json`. Real account values should remain local and
must not be committed.

Portfolio Agent now distinguishes wallet-level account value from verified
derivatives positions, so a partial MCP snapshot cannot be mislabeled as a
fully verified flat portfolio.
