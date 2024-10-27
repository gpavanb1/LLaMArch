from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass
import logging


@dataclass
class AgentResponse:
    """Data class to store agent responses"""
    agent_id: str
    response: Any
    confidence: float
    metadata: Dict[str, Any]


class GenerativeAIAgent(ABC):
    def __init__(self, agent_id: str, model_name: str):
        self.agent_id = agent_id
        self.model_name = model_name
        self.performance_history: List[float] = []
        self.logger = logging.getLogger(f"Agent-{agent_id}")

    @abstractmethod
    async def generate_response(self, query: str) -> AgentResponse:
        """Generate a response for the given query"""
        pass

    def update_performance(self, score: float):
        """Update agent's performance history"""
        self.performance_history.append(score)
        self.logger.info(f"Agent {self.agent_id} performance updated: {score}")

    @property
    def average_performance(self) -> float:
        """Calculate agent's average performance"""
        return np.mean(self.performance_history) if self.performance_history else 0.0
