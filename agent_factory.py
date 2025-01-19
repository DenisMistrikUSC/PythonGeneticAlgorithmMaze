from typing import Type
from geneticagent_naive import GeneticAgentNaive
from geneticagent_virtual import GeneticAgent

class AgentFactory:
    _agent_mapping = {
        "naive" : GeneticAgentNaive
    }

    def create_agent(self, type, sequence_length, speed, start, turn_rate):
        type = type.lower()
        agent_class: Type[GeneticAgent] = self._agent_mapping.get(type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {type}")

        return agent_class(sequence_length, speed, start, turn_rate)