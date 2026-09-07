from .base import BaseAgent, AgentOutput


class DecisionAgent(BaseAgent):
    name = "Decision Agent"

    def run(self, context):
        market = context["market"]
        risk = context["risk"]
        portfolio = context["portfolio"]

        regime = market["regime"]
        score = risk["score"]

        if score >= 75:
            action = "NO_TRADE"
            summary = "Risk is too elevated for a new discretionary position."
        elif regime == "BULLISH_MOMENTUM":
            action = "WATCH_LONG"
            summary = "Momentum is positive, but entry should wait for confirmation."
        elif regime == "BEARISH_MOMENTUM":
            action = "WATCH_SHORT"
            summary = "Momentum is negative, but entry should wait for confirmation."
        else:
            action = "WAIT"
            summary = "No sufficiently asymmetric setup is detected."

        confidence = round(max(0.5, min(0.95, 1 - score / 160)), 2)

        data = {
            "action": action,
            "summary": summary,
            "why": (
                f"Regime={regime}; risk={score}/100; "
                f"portfolio={portfolio['state']}."
            ),
            "invalidation": "Invalidate the proposal if the market regime flips or risk score materially increases.",
            "entry_logic": "Require independent confirmation before any order is considered.",
            "stop_logic": "Define a hard invalidation level before execution; never widen risk after entry.",
            "confidence": confidence,
        }

        message = f"Decision {action} with confidence {confidence:.2f}; execution remains blocked."
        return AgentOutput(self.name, data, message)
