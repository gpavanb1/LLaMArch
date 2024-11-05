# memory_decay.py

from typing import Any


class MemoryDecay:
    def __init__(self, importance_threshold=0.5):
        """
        Initialize memory decay/evaluation component with an importance threshold.

        Args:
            importance_threshold (float): Threshold for deciding if information is important enough to retain.
        """
        self.importance_threshold = importance_threshold

    def evaluate(self, summary: str) -> bool:
        """
        Evaluate if a summary is important enough to store in Long-Term Memory.

        Args:
            summary (str): The summarized text to evaluate.

        Returns:
            bool: True if the information should be stored in Long-Term Memory, False otherwise.
        """
        # Example heuristic: Check if certain keywords are in the summary
        important_keywords = ["important", "critical", "relevant", "necessary"]
        score = sum(1 for word in important_keywords if word in summary.lower(
        )) / len(important_keywords)

        # Decision based on threshold
        return score >= self.importance_threshold
