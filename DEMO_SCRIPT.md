# 90-Second Demo Script

## Scene 1 — 0:00–0:10

Show the dashboard.

Say:

"Most AI trading demos start with a BUY or SELL button. Binance Risk Sentinel starts one step earlier: should an agent be allowed to trade at all?"

## Scene 2 — 0:10–0:30

Run a BTCUSDT scan.

Say:

"Four agents independently evaluate the state. Market Agent identifies regime and volatility. Risk Agent converts that state into a risk score and position-size constraint."

## Scene 3 — 0:30–0:45

Point to the trace.

Say:

"Portfolio Agent checks existing exposure, and Decision Agent combines the evidence. Every conclusion is visible instead of being a black box."

## Scene 4 — 0:45–1:05

Paste an Agent OS snapshot.

Say:

"When account context comes from an authenticated Binance Agent OS-compatible session, the portfolio layer can become account-aware without putting credentials into this dashboard."

## Scene 5 — 1:05–1:20

Point to Human Confirmation.

Say:

"The key design decision is here: analysis is automated, but authorization is not. The dashboard cannot silently turn a recommendation into an order."

## Scene 6 — 1:20–1:30

Show MCP setup.

Say:

"The execution layer is intentionally delegated to the Binance Agent OS MCP-compatible client, where permissions and human confirmation remain under user control."
