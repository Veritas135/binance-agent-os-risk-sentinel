from .base import BaseAgent, AgentOutput
from data.binance_public import BinancePublicMarket


def _num(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class MarketAgent(BaseAgent):
    name = "Market Agent"

    def run(self, context):
        symbol = context["symbol"]
        demo = context["demo_mode"]
        snapshot = context.get("snapshot") or {}

        mcp_market = snapshot.get("market") or {}
        snapshot_symbol = str(mcp_market.get("symbol", "")).upper()

        if mcp_market and snapshot_symbol == symbol.upper():
            last_price = _num(mcp_market.get("lastPrice", mcp_market.get("last_price")))
            change = _num(mcp_market.get("priceChangePercent", mcp_market.get("change_pct")))
            high = _num(mcp_market.get("highPrice", mcp_market.get("high")))
            low = _num(mcp_market.get("lowPrice", mcp_market.get("low")))
            volume = _num(mcp_market.get("volume"))
            quote_volume = _num(mcp_market.get("quoteVolume", mcp_market.get("quote_volume")))
            range_pct = ((high - low) / low * 100) if low > 0 else 0.0
            market = {
                "symbol": symbol,
                "last_price": last_price,
                "change_pct": change,
                "high": high,
                "low": low,
                "volume": volume,
                "quote_volume": quote_volume,
                "range_pct": range_pct,
                "source": snapshot.get("source", "Binance Agent OS MCP"),
            }
        else:
            market = BinancePublicMarket().ticker_24h(symbol, demo=demo)
            market["source"] = "demo fixture" if demo else "Binance public REST"

        change = market["change_pct"]
        range_pct = market["range_pct"]

        if range_pct >= 8:
            regime = "HIGH_VOLATILITY"
        elif change >= 2:
            regime = "BULLISH_MOMENTUM"
        elif change <= -2:
            regime = "BEARISH_MOMENTUM"
        else:
            regime = "NEUTRAL"

        market["regime"] = regime
        message = (
            f"{symbol}: {regime}; 24h {change:.2f}%, "
            f"range proxy {range_pct:.2f}%; source={market['source']}."
        )
        return AgentOutput(self.name, market, message)
