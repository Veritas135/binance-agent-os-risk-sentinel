from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from .market_agent import MarketAgent
from .risk_agent import RiskAgent
from .portfolio_agent import PortfolioAgent
from .decision_agent import DecisionAgent


@dataclass
class SentinelResult:
    market: Dict[str, Any]
    risk: Dict[str, Any]
    portfolio: Dict[str, Any]
    decision: Dict[str, Any]
    trace: List[Dict[str, str]]

    def to_dict(self):
        return asdict(self)


class Orchestrator:
    def run(
        self,
        symbol: str,
        risk_budget_pct: float,
        demo_mode: bool = True,
        snapshot: Optional[Dict[str, Any]] = None,
    ) -> SentinelResult:
        context = {
            "symbol": symbol,
            "risk_budget_pct": risk_budget_pct,
            "demo_mode": demo_mode,
            "snapshot": snapshot,
        }

        trace = []

        market_out = MarketAgent().run(context)
        context["market"] = market_out.data
        trace.append({"agent": market_out.agent, "message": market_out.message})

        risk_out = RiskAgent().run(context)
        context["risk"] = risk_out.data
        trace.append({"agent": risk_out.agent, "message": risk_out.message})

        portfolio_out = PortfolioAgent().run(context)
        context["portfolio"] = portfolio_out.data
        trace.append({"agent": portfolio_out.agent, "message": portfolio_out.message})

        decision_out = DecisionAgent().run(context)
        context["decision"] = decision_out.data
        trace.append({"agent": decision_out.agent, "message": decision_out.message})

        return SentinelResult(
            market=market_out.data,
            risk=risk_out.data,
            portfolio=portfolio_out.data,
            decision=decision_out.data,
            trace=trace,
        )
