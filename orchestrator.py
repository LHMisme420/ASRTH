# swarm/orchestrator.py
from typing import List
from agents.base import AttackAttempt, AttackAgent

class Swarm:
    def __init__(self, agents: List[AttackAgent]):
        self.agents = agents

    def generate_attacks(self, llm, context: str) -> List[AttackAttempt]:
        return [agent.generate(llm, context) for agent in self.agents]

