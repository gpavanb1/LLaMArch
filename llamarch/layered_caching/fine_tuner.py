class FineTuner:
    def __init__(self, model):
        self.model = model

    def fine_tune(self, data):
        # Fine-tune the smaller model with the provided data
        # This is a placeholder, actual fine-tuning would involve more steps
        self.model.train(data)
        return self.model
