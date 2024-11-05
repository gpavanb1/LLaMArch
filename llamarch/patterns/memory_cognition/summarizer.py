from typing import List, Union

MAX_LENGTH = 300


class Summarizer:
    def __init__(self, llm: 'LLM'):
        """
        Initialize the Summarizer with an LLM instance.

        Args:
            llm (LLM): An instance of the LLM class for generating summaries.
        """
        self.llm = llm

    def summarize(self, items: List[Union[dict, str]]) -> str:
        """
        Summarize a list of items.

        Args:
            items (List[Union[dict, str]]): List of items to summarize.

        Returns:
            str: The generated summary.
        """
        # Extract text content from items and concatenate it for summarization
        text = " ".join([item if isinstance(item, str)
                         else getattr(item, "metadata", "").get("query") for item in items])
        text = text[:MAX_LENGTH]

        # Use the LLM instance to generate the summary
        prompt = f"Please summarize the following text:\n{text}\nSummary:"
        summary = self.llm.generate(prompt)

        return summary
