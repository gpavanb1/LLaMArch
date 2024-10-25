import torch
import torch.nn as nn
from transformers import AutoModel


class MultiTaskModel(nn.Module):
    def __init__(self, model_name, task_heads: dict):
        """
        :param model_name: Pre-trained foundational model name (e.g., 'bert-base-uncased').
        :param task_heads: Dictionary mapping task names to task-specific heads.
                           Example: {"task_a": TaskAHead(), "task_b": TaskBHead()}.
        """
        super(MultiTaskModel, self).__init__()

        # Load a pretrained foundational LLM (like BERT, GPT, etc.)
        self.shared_model = AutoModel.from_pretrained(model_name)
        self.shared_representation = nn.Linear(
            self.shared_model.config.hidden_size, 256)

        # Dictionary of task-specific heads
        self.task_heads = nn.ModuleDict(task_heads)

    def forward(self, input_data, task_name):
        """
        :param input_data: Input data (tokenized) for the model.
        :param task_name: The specific task for which the model is generating output.
        """
        # Extract shared representation using the foundational model
        outputs = self.shared_model(**input_data)
        shared_representation = self.shared_representation(
            outputs.last_hidden_state[:, 0, :])

        # Forward through the task-specific head
        if task_name in self.task_heads:
            task_output = self.task_heads[task_name](shared_representation)
            return task_output
        else:
            raise ValueError(
                f"Task '{task_name}' is not defined in task heads.")
