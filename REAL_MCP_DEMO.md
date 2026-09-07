# Real Binance Agent OS / MCP Demo

This document explains how to demonstrate **real Binance MCP data** without committing private account information.

## Evidence chain

```text
ChatGPT / compatible agent
        ↓
Binance Agent OS MCP
        ↓
real market + account context
        ↓
Binance Risk Sentinel
        ↓
Market → Risk → Portfolio → Decision
        ↓
BLOCKED_UNTIL_HUMAN_CONFIRMATION
```

## 1. Read real market data

In an authenticated Binance MCP session, request:

> Query the BTCUSDT 24-hour ticker. Read only. Do not trade.

Use the returned price, 24-hour percentage change, high and low as evidence that the MCP connection is live.

## 2. Read account context

Request:

> Query my Binance wallet values in USDT and, separately, my open derivatives positions. Read only. Do not place or modify orders.

Do **not** paste API keys, passwords, cookies, recovery codes, or authentication tokens into the repository.

## 3. Build a local snapshot

The dashboard accepts this schema:

```json
{
  "source": "Binance Agent OS MCP",
  "wallets": [
    {
      "walletName": "Spot",
      "quoteAsset": "USDT",
      "value": "YOUR_RETURNED_VALUE"
    }
  ],
  "positions": [],
  "metadata": {
    "positions_verified": false
  }
}
```

If the MCP call has separately verified the positions list, set:

```json
"positions_verified": true
```

Never mark positions as verified merely because the list is empty.

## 4. Paste into the dashboard

Open the Streamlit sidebar and paste the JSON into **Optional MCP snapshot**.

Run **Sentinel Scan**.

Portfolio Agent distinguishes among:

- `DERIVATIVES_EXPOSED`
- `ASSET_BALANCE_PRESENT`
- `WALLET_VALUE_PRESENT`
- `FLAT`
- `ACCOUNT_CONTEXT_PARTIAL`

This prevents the system from falsely interpreting a partial wallet snapshot as a verified flat portfolio.

## 5. Recording rule

For a public hackathon video, you may blur or crop exact account balances if you prefer.

The important evidence is:

1. the Binance MCP tool returns real data;
2. Sentinel accepts structured MCP context;
3. the multi-agent reasoning changes based on account state;
4. execution remains blocked until explicit human confirmation.

## Public repository policy

`data/example_mcp_snapshot.json` is intentionally fictional and safe for the public repository.

Do not commit a real account snapshot.
