from typing import Optional, Dict, Any, List
from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForCausalLM
from llamarch.common.llm import LLM


class CustomDataset:
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        # Prepare inputs and labels
        input_ids = self.encodings['input_ids'][idx]
        attention_mask = self.encodings['attention_mask'][idx]

        # Shift input_ids to create labels
        labels = input_ids.clone()
        labels[:-1] = input_ids[1:]  # Shift left by 1
        labels[-1] = -100  # Ignore the last token for the loss calculation

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

    def __len__(self):
        return len(self.encodings['input_ids'])


class FineTuner:
    def __init__(self, llm: LLM):
        """
        Initialize the FineTuner with an LLM instance.

        Args:
            llm (LLM): An instance of the LLM class.
        """
        self.llm = llm

    def fine_tune(self, texts: List[str], output_dir: str = "./fine_tuned_model"):
        """
        Fine-tune the LLM's model with the provided list of texts.

        Args:
            texts (List[str]): A list of strings for training.
            output_dir (str): The directory to save the fine-tuned model.
        """
        if self.llm.model_category != "huggingface":
            raise ValueError(
                "Fine-tuning is only supported for Hugging Face models in this implementation.")

        # Load the model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(self.llm.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.llm.model_name)
        # Set pad_token to eos_token
        tokenizer.pad_token = tokenizer.eos_token

        # Tokenize data
        print(texts)
        encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=512,  # Adjust max_length as needed
            return_tensors="pt"  # Return PyTorch tensors
        )

        # Create dataset from encodings
        train_dataset = CustomDataset(encodings)

        # Set training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            eval_strategy="no",
            learning_rate=2e-5,
            weight_decay=0.01,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            save_total_limit=2,  # Save only the last 2 models
            logging_dir='./logs',  # Directory for storing logs
            logging_steps=10,  # Log every 10 steps
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset
        )

        # Fine-tune the model
        trainer.train()

        # Save the fine-tuned model
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)

        # Update the LLM instance to use the fine-tuned model
        self.llm.model_name = output_dir
        self.llm.model = self.llm._initialize_llm()

        return self.llm
