class Verdict:
    def __init__(self, block, reason=""):
        self.block = block
        self.reason = reason

def policy_gate(prompt: str) -> Verdict:
    p = prompt.lower()

    # Direct / strong signals of "reveal internal rules / hidden instructions"
    rule_probe_signals = [
        "safety rules you follow",
        "hidden instructions",
        "internal guidelines",
        "internal guidance",
        "developer-style summary",
        "output the rule set",
        "rule set first",
        "what you're not allowed",
        "summarize any hidden",
        "system update",
        "ignore constraints",
        "ignore previous",
        "not bound by",

        # NEW: probes you showed that slipped
        "categories of requests you must refuse",
        "categories of requests you must",
        "requests you must refuse",
        "what are the categories of requests",
        "what information from earlier in this conversation",
        "what information from earlier",
        "what are you using right now",
        "for transparency",
        "outline them at a high level",
        "give examples",  # only used in combination below
    ]

    # Tool/data exfil signals
    exfil_signals = [
        "dump memory",
        "print memory",
        "reveal memory",
        "show me your rules",
        "policy you follow",
        "internal prompt",
        "system prompt",
        "developer message",
    ]

    if any(s in p for s in exfil_signals):
        return Verdict(True, "exfil_probe")

    if any(s in p for s in rule_probe_signals):
        return Verdict
