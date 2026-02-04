# swarm/evolution.py
import random
from typing import List, Tuple
from agents.base import AttackAttempt

def mutate(text: str) -> str:
    # Simple mutation starter (we'll upgrade later)
    swaps = [
        ("ignore previous", "disregard prior"),
        ("policy", "rules"),
        ("secret", "hidden"),
        ("exfiltrate", "extract"),
        ("system prompt", "internal prompt"),
    ]
    for a, b in swaps:
        if a in text.lower() and random.random() < 0.5:
            return text.lower().replace(a, b)
    # fallback: add harmless noise
    return text + "\n\n(Answer in a concise format.)"

def evolve(population: List[AttackAttempt], scores: List[float]) -> List[AttackAttempt]:
    ranked: List[Tuple[AttackAttempt, float]] = sorted(
        zip(population, scores), key=lambda x: x[1], reverse=True
    )
    if not ranked:
        return population

    survivors = [a for a, _ in ranked[: max(1, len(ranked)//2)]]
    children: List[AttackAttempt] = []

    for s in survivors:
        children.append(AttackAttempt(agent=s.agent, prompt=mutate(s.prompt)))

    # keep size stable
    next_pop = survivors + children
    return next_pop[: len(population)]

