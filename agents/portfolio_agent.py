from .base import BaseAgent, AgentOutput


def _number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


class PortfolioAgent(BaseAgent):
    name = "Portfolio Agent"

    def run(self, context):
        snapshot = context.get("snapshot")

        if not snapshot:
            data = {
                "state": "FLAT_DEMO",
                "open_positions": 0,
                "nonzero_balance_entries": 0,
                "wallet_value_quote": 0.0,
                "positions_verified": False,
                "source": "demo portfolio",
            }
            return AgentOutput(
                self.name,
                data,
                "Portfolio state FLAT_DEMO from demo portfolio; no authenticated account snapshot supplied.",
            )

        positions = snapshot.get("positions") or []
        balances = snapshot.get("balances") or []
        wallets = snapshot.get("wallets") or []
        metadata = snapshot.get("metadata") or {}

        open_positions = [
            p for p in positions
            if abs(_number(p.get("positionAmt", p.get("amount", 0)))) > 0
        ]

        nonzero_balances = [
            b for b in balances
            if abs(_number(b.get("free", 0))) + abs(_number(b.get("locked", 0))) > 0
            or abs(_number(b.get("balance", 0))) > 0
        ]

        active_wallets = [
            w for w in wallets
            if abs(_number(w.get("value", w.get("balance", 0)))) > 0
        ]
        wallet_value_quote = sum(
            _number(w.get("value", w.get("balance", 0))) for w in active_wallets
        )

        positions_verified = bool(metadata.get("positions_verified", False))

        if open_positions:
            state = "DERIVATIVES_EXPOSED"
        elif nonzero_balances:
            state = "ASSET_BALANCE_PRESENT"
        elif active_wallets:
            state = "WALLET_VALUE_PRESENT"
        elif positions_verified:
            state = "FLAT"
        else:
            state = "ACCOUNT_CONTEXT_PARTIAL"

        source = snapshot.get("source", "Agent OS MCP snapshot")
        data = {
            "state": state,
            "open_positions": len(open_positions),
            "nonzero_balance_entries": len(nonzero_balances),
            "wallet_value_quote": round(wallet_value_quote, 8),
            "positions_verified": positions_verified,
            "source": source,
        }

        verification_note = (
            "positions verified" if positions_verified
            else "derivatives positions not verified by this snapshot"
        )
        message = (
            f"Portfolio state {state}; {len(open_positions)} open derivative position(s); "
            f"{len(nonzero_balances)} non-zero asset balance entrie(s); "
            f"wallet value field={wallet_value_quote:.8f}; {verification_note}."
        )
        return AgentOutput(self.name, data, message)
