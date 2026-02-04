from base import AttackAttempt

class Swarm:
    def __init__(self, agents):
        self.agents = agents

    def generate_attacks(self, llm, context):
        attacks = []
        for agent in self.agents:
            attacks.append(agent.generate(llm, context))
        return attacks
