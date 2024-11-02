import asyncio
from .consensus import ConsensusLayer, OutputAggregator


class AgentSwarm:
    def __init__(self, agent_list):
        self.agent_list = agent_list
        self.consensus_layer = ConsensusLayer()
        self.aggregator = OutputAggregator()

    async def _gather_responses(self, agent_list, query):
        return await asyncio.gather(*(a.generate_response(query) for a in agent_list))

    def run_iteration(self, query):
        # Get the consensus
        responses = asyncio.run(self._gather_responses(self.agent_list, query))
        consensus_result = self.consensus_layer.get_consensus(
            responses, self.agent_list)
        output = self.aggregator.aggregate_output(consensus_result)

        return output
