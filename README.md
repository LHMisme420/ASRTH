# ASRTH — Adversarial Swarm Red-Team Harness

Multi-agent evolutionary framework designed to pressure-test **runtime overlays**, **policy gates**, and **jailbreak defenses** in LLMs and agentic systems.

Swarm of specialized agents collaboratively evolves adversarial prompts/strategies to bypass safeguards — async, evolvable, measurable.

**Status**: Early prototype / research harness (proof-of-concept stage)

## Core Idea

Many agents with different roles (jailbreakers, drifters, evaluators, mutators) run in parallel → evolve attack chains over generations → find weak points in policy enforcement layers.

Inspired by: evolutionary algorithms + multi-agent debate + red-teaming swarms.

## Features (current)

- Asynchronous agent swarm orchestration
- Evolutionary prompt/strategy mutation
- Context rollover & memory drift simulation
- Policy gate simulation + guarded LLM wrapper
- Success/failure counters & basic metrics
- Modular agent types (jailbreaker, drift, etc.)

## Requirements

- Python 3.10+
- (Add your actual deps here once you have requirements.txt)

## Quick Start (Local)

```bash
git clone https://github.com/LHMisme420/ASRTH.git
cd ASRTH
pip install -r requirements.txt          # create this file first
python run_harness.py
ASRTH/
├── agents/             # agent role implementations
├── vata/               # (likely variation / attack tree logic)
├── base.py             # core abstractions
├── orchestrator.py     # swarm coordinator
├── evolution.py        # mutation & selection logic
├── guarded_llm.py      # policy-wrapped LLM interface
├── policy_gate.py      # simulated defense layer
├── jailbreaker.py      # primary attack agent
├── drift_agent.py      # context/memory drift agent
├── context_rollover.py # long-conversation simulation
├── counters.py         # metrics tracking
├── run_harness.py      # main entry point
├── PROJECT_PRINCIPLES.md
└── SPEC_ARTIFACT_FORMAT.md
