import asyncio
from .agent_selector import AgentSelector
from .output_integrator import OutputIntegrator
from .feedback import FeedbackMechanism


class MultiAgentModel:
    def __init__(self, agent_list):
        """
        Initialize components of the multi-agent model.
        """
        # Instantiate agents
        self.agent_list = agent_list
        self.selector = AgentSelector(self.agent_list)
        self.integrator = OutputIntegrator()

    async def _gather_responses(self, agent_list, query):
        return await asyncio.gather(*(a.generate_response(query) for a in agent_list))

    def process_query(self, query):
        """
        Process the query through the multi-agent system.
        """
        # Step 1: Select agents based on the query
        selected_agents = self.selector.select_agents(query)

        # Step 2: Each selected agent generates an output
        responses = asyncio.run(self._gather_responses(selected_agents, query))

        # Step 3: Integrate outputs from all agents
        unified_output = self.integrator.integrate_outputs(responses)

        # # Step 4: Collect feedback and adjust rules as needed
        feedback = f"Feedback for query '{query}': output quality needs improvement."
        self.feedback_mechanism.collect_feedback(feedback)
        self.feedback_mechanism.adjust_rules()

        return unified_output
