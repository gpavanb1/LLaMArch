import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from multitask_model import MultiTaskModel

# Example task heads (for illustration purposes, define task heads in another file)


class GenericTaskHead(torch.nn.Module):
    def __init__(self, output_size):
        super(GenericTaskHead, self).__init__()
        self.classifier = torch.nn.Linear(256, output_size)

    def forward(self, x):
        return self.classifier(x)

# Prepare generalized data loaders (you can expand this for your own dataset)


def get_data_loaders(tasks):
    """
    Create data loaders for each task dynamically.
    :param tasks: Dictionary where keys are task names and values are task-specific datasets.
    :return: A dictionary of DataLoader objects for each task.
    """
    task_loaders = {}
    for task_name, dataset in tasks.items():
        task_loaders[task_name] = DataLoader(
            dataset, batch_size=32, shuffle=True)
    return task_loaders
