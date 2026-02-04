import random
from agents.base import AttackAttempt

def mutate(text):
    return text.replace("policy", "rules")

def evolve(population, scores):
    ranked = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
    survivors = [a for a,_ in ranked[:max(1,len(ranked)//2)]]
    children = [AttackAttempt(a.agent, mutate(a.prompt)) for a in survivors]
    return (survivors + children)[:len(population)]
