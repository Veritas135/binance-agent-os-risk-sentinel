from .base import BaseAgent, AgentOutput


class RiskAgent(BaseAgent):
    name = "Risk Agent"

    def run(self, context):
        market = context["market"]
        budget = context["risk_budget_pct"]

        score = 25.0
        score += min(abs(market["change_pct"]) * 5, 30)
        score += min(market["range_pct"] * 4, 35)

        if market["regime"] == "HIGH_VOLATILITY":
            score += 10

        score = min(100.0, round(score, 1))
        size_factor = max(0.25, 1.25 - score / 100)
        max_notional_pct = round(budget * 100 * size_factor, 2)

        data = {
            "score": score,
            "size_factor": round(size_factor, 2),
            "max_notional_pct": max_notional_pct,
        }
        message = (
            f"Risk score {score}/100; sizing factor {size_factor:.2f}×; "
            f"max proposed notional {max_notional_pct:.2f}%."
        )
        return AgentOutput(self.name, data, message)
