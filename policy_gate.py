# overlay/policy_gate.py
from dataclasses import dataclass

@dataclass
class Verdict:
    block: bool
    reason: str = ""

def policy_gate(prompt: str) -> Verdict:
    p = prompt.lower()

    # Starter rules (upgrade later with intent classifier + embeddings)
    jailbreak_markers = [
        "ignore previous",
        "disregard prior",
        "you are not bound",
        "system prompt",
        "developer message",
        "reveal hidden",
        "jailbreak",
    ]
    exfil_markers = [
        "exfiltrate",
        "extract secrets",
        "leak",
        "show me your rules",
        "print your policy",
        "dump memory",
    ]

    if any(m in p for m in jailbreak_markers):
        return Verdict(True, "jailbreak_marker")

    if any(m in p for m in exfil_markers):
        return Verdict(True, "exfil_marker")

    return Verdict(False, "")

