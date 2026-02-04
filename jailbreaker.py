# agents/jailbreaker.py
from agents.base import AttackAgent

class Jailbreaker(AttackAgent):
    def __init__(self):
        super().__init__(
            name="jailbreaker",
            persona="expert in prompt injection, role confusion, policy bypass phrasing"
        )

