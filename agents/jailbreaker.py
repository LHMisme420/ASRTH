from agents.base import AttackAgent

class Jailbreaker(AttackAgent):
    def __init__(self):
        super().__init__(
            "jailbreaker",
            "expert in prompt injection, role confusion, sandbox escape"
        )
