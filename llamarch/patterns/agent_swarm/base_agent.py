from typing import Dict, List, Any, Optional
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding
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


class GenerativeAIAgent:
    def __init__(self, agent_id: str, llm: LLM, embedding: LLMEmbedding):
        """
        Initialize a generative AI agent.

        Args:
            agent_id (str): Unique identifier for the agent.
            llm (LLM): An instance of the LLM class, initialized with the desired model.
            embedding (LLMEmbedding): An instance of the LLMEmbedding class, initialized with the desired embedding model.
        """
        self.agent_id = agent_id
        self.llm = llm
        self.embedding = embedding
        self.performance_history: List[float] = []
        self.logger = logging.getLogger(f"Agent-{agent_id}")

    async def generate_response(self, query: str) -> AgentResponse:
        """
        Generate a response for the given query using the language model.

        Args:
            query (str): The input query to respond to.
            max_tokens (int): Maximum tokens for the response.
            temperature (float): The temperature parameter for controlling randomness.

        Returns:
            AgentResponse: An object containing the response and metadata.
        """
        response_text = self.llm.generate(query)
        confidence = 1.0  # Placeholder; this could be dynamically calculated if desired
        metadata = {
            "model_name": self.llm.model_name
        }
        return AgentResponse(agent_id=self.agent_id, response=response_text, confidence=confidence, metadata=metadata)

    def update_performance(self, score: float):
        """Update agent's performance history"""
        self.performance_history.append(score)
        self.logger.info(f"Agent {self.agent_id} performance updated: {score}")

    @property
    def average_performance(self) -> float:
        """Calculate agent's average performance"""
        return np.mean(self.performance_history) if self.performance_history else 0.0
