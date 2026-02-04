class RollingContext:
    def __init__(self, max_tokens=1200):
        self.max_tokens = max_tokens
        self.messages = []

    def add(self, role, text):
        self.messages.append((role, text))
        self._trim()

    def _trim(self):
        joined = []
        total = 0
        for r, t in reversed(self.messages):
            total += len(t)
            joined.append((r, t))
            if total >= self.max_tokens:
                break
        self.messages = list(reversed(joined))

    def render(self):
        return "\n".join([f"{r}: {t}" for r, t in self.messages])
