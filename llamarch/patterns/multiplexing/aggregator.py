class OutputAggregator:
    def aggregate(self, outputs):
        # Simply concatenates outputs for now, but could apply more sophisticated aggregation logic
        return " | ".join(outputs)
