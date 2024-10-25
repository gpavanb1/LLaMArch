from general_purpose_llm import GeneralPurposeLLM
from context_understanding import ContextUnderstanding
from specialized_submodels import DomainModels
from aggregator import OutputAggregator


class SystemController:
    def __init__(self, api_key):
        self.general_llm = GeneralPurposeLLM(api_key)
        self.context_und = ContextUnderstanding()
        self.domain_models = DomainModels()
        self.aggregator = OutputAggregator()

    def handle_query(self, query):
        # Step 1: Use General Purpose LLM to process query and get context
        context = self.general_llm.process_query(query)

        # Step 2: Use ContextUnderstanding to determine which domain models to use
        domain = self.context_und.determine_domain(context)
        specialized_model = self.domain_models.get_model(domain)

        if specialized_model:
            # Step 3: Query the specialized model
            output = specialized_model.query(query)

            # Step 4: Aggregate the output (if querying multiple models, this can be extended)
            final_output = self.aggregator.aggregate([output])
            return final_output
        else:
            return "No specialized model found for this query"
