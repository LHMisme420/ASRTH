# runtime/guarded_llm.py
from overlay.policy_gate import policy_gate

def guarded_call(llm, prompt: str, metrics: dict):
    verdict = policy_gate(prompt)
    if verdict.block:
        metrics["blocked"] += 1
        metrics["blocked_reasons"][verdict.reason] = metrics["blocked_reasons"].get(verdict.reason, 0) + 1
        return "[BLOCKED]"
    metrics["allowed"] += 1
    return llm(prompt)

