from .base import BaseAgent, AgentOutput
from data.binance_public import BinancePublicMarket


class MarketAgent(BaseAgent):
    name = "Market Agent"

    def run(self, context):
        symbol = context["symbol"]
        demo = context["demo_mode"]
        market = BinancePublicMarket().ticker_24h(symbol, demo=demo)

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
            f"range proxy {range_pct:.2f}%."
        )
        return AgentOutput(self.name, market, message)
