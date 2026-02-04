class Verdict:
    def __init__(self, block, reason=""):
        self.block = block
        self.reason = reason

def policy_gate(prompt):
    p = prompt.lower()

    if "ignore previous" in p:
        return Verdict(True, "jailbreak")

    if "exfiltrate" in p or "leak" in p:
        return Verdict(True, "exfiltration")

    return Verdict(False)
