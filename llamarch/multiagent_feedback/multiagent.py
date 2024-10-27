from generative_ai_agent import GenerativeAIAgent
from agent_selector import AgentSelector
from output_integrator import OutputIntegrator
from feedback_mechanism import FeedbackMechanism


class MultiAgentModel:
    def __init__(self):
        """
        Initialize components of the multi-agent model.
        """
        # Instantiate agents
        self.agents = [
            GenerativeAIAgent("Agent_1"),
            GenerativeAIAgent("Agent_2"),
            GenerativeAIAgent("Agent_3")
        ]
        self.selector = AgentSelector(self.agents)
        self.integrator = OutputIntegrator()
        self.feedback_mechanism = FeedbackMechanism()

    def process_query(self, query):
        """
        Process the query through the multi-agent system.
        """
        # Step 1: Select agents based on the query
        selected_agents = self.selector.select_agents(query)

        # Step 2: Each selected agent generates an output
        outputs = [agent.generate_output(query) for agent in selected_agents]

        # Step 3: Integrate outputs from all agents
        unified_output = self.integrator.integrate_outputs(outputs)

        # Step 4: Collect feedback and adjust rules as needed
        feedback = f"Feedback for query '{query}': output quality needs improvement."
        self.feedback_mechanism.collect_feedback(feedback)
        self.feedback_mechanism.adjust_rules()

        return unified_output
