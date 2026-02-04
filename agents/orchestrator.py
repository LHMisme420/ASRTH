from agents.base import AttackAttempt

class Swarm:
    def __init__(self, agents):
        self.agents = agents

    def generate_attacks(self, llm, context):
        return [agent.generate(llm, context) for agent in self.agents]
