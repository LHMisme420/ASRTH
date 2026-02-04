from overlay.policy_gate import policy_gate

def guarded_call(llm, prompt, metrics):
    verdict = policy_gate(prompt)

    if verdict.block:
        metrics["blocked"] += 1
        return "[BLOCKED]"

    metrics["allowed"] += 1
    return llm(prompt)
