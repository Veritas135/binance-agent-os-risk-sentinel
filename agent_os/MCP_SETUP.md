# Binance Agent OS / MCP Setup

This project intentionally does **not** embed Binance API keys or MCP credentials in Streamlit.

The intended production path is:

`Agent OS-compatible client → Binance MCP → Risk Sentinel reasoning → human confirmation → supported Binance action`

## Official MCP endpoint

`https://agent.binance.com/mcp/agentic`

## Claude Code

Use the official MCP endpoint in your Claude Code environment:

```bash
claude mcp add binance-mcp-server --transport http https://agent.binance.com/mcp/agentic
```

Then load `agent_os/system_prompt.md` as the project's operating instructions.

## Other compatible clients

The Binance documentation lists compatible AI agent environments including Claude Code, Claude, Codex, ChatGPT and VS Code. The exact UI/authentication flow can change, so use Binance's current Agent OS documentation when connecting.

## Streamlit demo

The Streamlit dashboard has two independent data paths:

- Demo mode: deterministic fixture data.
- Live public mode: Binance public REST 24h ticker data.

For account-aware analysis, paste a JSON snapshot returned by your authenticated Agent OS-compatible client into the optional sidebar field. The app labels that data as an Agent OS MCP snapshot and does not invent missing fields.
