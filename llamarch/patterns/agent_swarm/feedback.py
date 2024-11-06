from typing import Dict, Any, List
from llamarch.common.base_agent import GenerativeAIAgent
import numpy as np
import logging
from datetime import datetime


class FeedbackMechanism:
    def __init__(self):
        self.feedback_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("FeedbackMechanism")

    def record_feedback(
        self,
        feedback: Dict[str, Any],
        agents: List[GenerativeAIAgent],
        consensus_data: Dict[str, Any]
    ):
        """Record and process feedback"""
        try:
            # Record feedback with timestamp
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "feedback": feedback,
                "consensus_data": consensus_data
            }
            self.feedback_history.append(feedback_entry)

            # Update agent performance scores
            self._update_agent_performance(feedback, agents, consensus_data)

            self.logger.info("Feedback processed and recorded successfully")

        except Exception as e:
            self.logger.error(f"Error processing feedback: {str(e)}")
            raise

    def _update_agent_performance(
        self,
        feedback: Dict[str, Any],
        agents: List[GenerativeAIAgent],
        consensus_data: Dict[str, Any]
    ):
        """Update performance metrics for all agents based on feedback"""
        try:
            # Calculate base score from feedback
            base_score = feedback.get("score", 0.0)

            # Get agreement matrix from consensus data
            agreement_matrix = np.array(consensus_data["agreement_matrix"])

            # Map agent IDs to their index in the contributing agents list
            agent_id_to_idx = {
                agent_id: idx
                for idx, agent_id in enumerate(consensus_data["contributing_agents"])
            }

            # Update each agent's performance
            for agent in agents:
                if agent.agent_id in agent_id_to_idx:
                    idx = agent_id_to_idx[agent.agent_id]

                    # Calculate agreement-based adjustment
                    agent_agreement = np.mean(agreement_matrix[idx])
                    adjusted_score = base_score * agent_agreement

                    # Update the agent's performance history
                    agent.update_performance(adjusted_score)

                    self.logger.info(
                        f"Updated performance for agent {agent.agent_id}: {adjusted_score}"
                    )

        except Exception as e:
            self.logger.error(f"Error updating agent performance: {str(e)}")
            raise

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a performance report based on feedback history"""
        try:
            return {
                "total_feedback_count": len(self.feedback_history),
                "recent_feedback": self.feedback_history[-5:],
                "average_feedback_score": np.mean([
                    f["feedback"].get("score", 0.0)
                    for f in self.feedback_history
                ])
            }
        except Exception as e:
            self.logger.error(f"Error generating performance report: {str(e)}")
            raise
