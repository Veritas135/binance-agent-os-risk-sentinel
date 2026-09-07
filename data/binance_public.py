import random
from typing import Dict

import requests


class BinancePublicMarket:
    BASE_URL = "https://api.binance.com/api/v3/ticker/24hr"

    def ticker_24h(self, symbol: str, demo: bool = True) -> Dict:
        if demo:
            return self._demo(symbol)

        response = requests.get(
            self.BASE_URL,
            params={"symbol": symbol},
            timeout=8,
        )
        response.raise_for_status()
        raw = response.json()

        high = float(raw["highPrice"])
        low = float(raw["lowPrice"])
        last = float(raw["lastPrice"])
        change = float(raw["priceChangePercent"])
        range_pct = ((high - low) / last * 100) if last else 0

        return {
            "symbol": symbol,
            "last_price": last,
            "change_pct": change,
            "range_pct": range_pct,
            "volume": float(raw["volume"]),
            "source": "Binance public REST API",
        }

    def _demo(self, symbol: str) -> Dict:
        presets = {
            "BTCUSDT": (106500, 2.8, 4.4),
            "ETHUSDT": (4400, 1.6, 5.2),
            "BNBUSDT": (820, -1.4, 3.8),
            "SOLUSDT": (205, -3.2, 8.7),
            "XRPUSDT": (2.9, 0.7, 4.9),
        }
        last, change, range_pct = presets.get(symbol, (100, 0, 4))
        jitter = random.uniform(-0.25, 0.25)
        return {
            "symbol": symbol,
            "last_price": last * (1 + jitter / 100),
            "change_pct": change + jitter,
            "range_pct": range_pct,
            "volume": 0,
            "source": "deterministic demo fixture",
        }
