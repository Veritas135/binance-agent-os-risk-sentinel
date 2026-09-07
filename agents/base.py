from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AgentOutput:
    agent: str
    data: Dict[str, Any]
    message: str


class BaseAgent:
    name = "BaseAgent"

    def run(self, context: Dict[str, Any]) -> AgentOutput:
        raise NotImplementedError
