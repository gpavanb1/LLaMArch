import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from multitask_model import MultiTaskModel
from task_head import GenericTaskHead


def main():
    # Example list of tasks
    task_configs = {
        # Binary classification
        "TaskA": {"output_size": 2, "loss_fn": torch.nn.CrossEntropyLoss()},
        "TaskB": {"output_size": 1, "loss_fn": torch.nn.MSELoss()},  # Regression
        # Multi-class classification
        "TaskC": {"output_size": 3, "loss_fn": torch.nn.CrossEntropyLoss()}
        # Add more tasks here as needed
    }

    model_name = "bert-base-uncased"

    # Dynamically create task heads and loss functions
    task_heads = {}
    loss_functions = {}

    for task_name, config in task_configs.items():
        task_heads[task_name] = GenericTaskHead(config["output_size"])
        loss_functions[task_name] = config["loss_fn"]

    # Initialize the multi-task model with the dynamically created task heads
    model = MultiTaskModel(model_name, task_heads)

    # Example optimizer (AdamW)
    optimizer = AdamW(model.parameters(), lr=1e-5)

    # Get data loaders for each task dynamically (replace with real datasets)
    task_datasets = {
        "TaskA": TaskADataset(),  # Replace with actual datasets
        "TaskB": TaskBDataset(),  # Replace with actual datasets
        "TaskC": TaskCDataset()   # Replace with actual datasets
        # Add more datasets as needed
    }
    task_loaders = get_data_loaders(task_datasets)

    # Set number of epochs
    epochs = 3  # For example

    # Generalized training loop for each task
    for epoch in range(epochs):
        model.train()

        for task_name, loader in task_loaders.items():
            for batch in loader:
                input_data, labels = batch
                optimizer.zero_grad()

                # Forward pass for the current task
                task_output = model(input_data, task_name)

                # Compute loss using the task-specific loss function
                loss = loss_functions[task_name](task_output, labels)
                loss.backward()
                optimizer.step()

        print(f"Epoch {epoch} completed.")
