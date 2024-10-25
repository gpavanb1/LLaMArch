class LowPowerLLM:
    def __init__(self, fine_tuned_model):
        self.model = fine_tuned_model

    def query(self, text):
        # Use the smaller fine-tuned model to answer queries
        return self.model(text)
