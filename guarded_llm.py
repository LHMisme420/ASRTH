from policy_gate import policy_gate

def guarded_call(llm, prompt, metrics):
    verdict = policy_gate(prompt)

    if verdict.block:
        metrics["blocked"] += 1
        metrics["blocked_reasons"][verdict.reason] = metrics["blocked_reasons"].get(verdict.reason, 0) + 1

        # Near-miss heuristic: long prompt + indirect phrasing = more dangerous
        if len(prompt) > 180 and ("please" in prompt.lower() or "help" in prompt.lower()):
            metrics["near_miss"] += 1

        return "[BLOCKED]"

    metrics["allowed"] += 1
    return llm(prompt)

