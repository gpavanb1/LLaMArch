from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from llamarch.common.base_agent import AgentResponse, GenerativeAIAgent
import logging


class ConsensusLayer:
    def __init__(self):
        self.logger = logging.getLogger("ConsensusLayer")

    def calculate_similarity_matrix(self, embeddings: List[List[float]]) -> np.ndarray:
        """Calculate similarity matrix from precomputed embeddings."""
        return cosine_similarity(embeddings)

    def get_consensus(self, responses: List[AgentResponse], agent_list: List[GenerativeAIAgent]) -> Dict[str, Any]:
        """Generate consensus from multiple agent responses."""
        try:
            # Extract response texts and compute embeddings using each agent's LLM instance
            response_texts = [r.response for r in responses]
            embeddings = [agent_list[r.agent_id].embedding.get_embeddings(
                r.response) for r in responses]

            # Calculate similarity matrix based on embeddings
            similarity_matrix = self.calculate_similarity_matrix(embeddings)

            # Calculate agreement scores
            agreement_scores = np.mean(similarity_matrix, axis=1)

            # Weight responses by agreement and confidence
            weighted_scores = [
                agreement_scores[i] * responses[i].confidence
                for i in range(len(responses))
            ]

            # Select best response based on weighted scores
            best_idx = np.argmax(weighted_scores)
            consensus_response = responses[best_idx].response

            return {
                "consensus_response": consensus_response,
                "confidence_score": weighted_scores[best_idx],
                "agreement_matrix": similarity_matrix.tolist(),
                "contributing_agents": [r.agent_id for r in responses]
            }
        except Exception as e:
            self.logger.error(f"Error in consensus generation: {str(e)}")
            raise


class OutputAggregator:
    def __init__(self):
        self.logger = logging.getLogger("OutputAggregator")

    def aggregate_output(self, consensus_result: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate and format the final output."""
        try:
            return {
                "final_response": consensus_result["consensus_response"],
                "metadata": {
                    "confidence": consensus_result["confidence_score"],
                    "contributing_agents": consensus_result["contributing_agents"],
                    "agreement_stats": {
                        "mean_agreement": np.mean(consensus_result["agreement_matrix"]),
                        "max_agreement": np.max(consensus_result["agreement_matrix"])
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error in output aggregation: {str(e)}")
            raise
