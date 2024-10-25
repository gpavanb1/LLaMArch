class QueryRouter:
    def __init__(self):
        self.agents: List[GenerativeAIAgent] = []
        self.logger = logging.getLogger("QueryRouter")

    def register_agent(self, agent: GenerativeAIAgent):
        """Register a new agent"""
        self.agents.append(agent)
        self.logger.info(f"Registered agent: {agent.agent_id}")

    async def route_query(self, query: str) -> List[AgentResponse]:
        """Route query to all registered agents"""
        responses = []
        for agent in self.agents:
            try:
                response = await agent.generate_response(query)
                responses.append(response)
            except Exception as e:
                self.logger.error(
                    f"Error from agent {agent.agent_id}: {str(e)}")
        return responses
