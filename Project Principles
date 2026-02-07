# VATA PROJECT PRINCIPLES

## 1. PURPOSE

VATA exists to produce probabilistic forensic measurements about digital content using reproducible, locally executable systems.

The system does NOT determine truth.
The system does NOT determine identity.
The system produces bounded statistical signals under explicit assumptions.

---

## 2. NON-GOALS

VATA will never:

- Claim to prove humanness
- Claim to prove authorship
- Claim to detect consciousness, soul, intent, or identity
- Claim perfect accuracy
- Claim immunity to adversarial attack

---

## 3. CORE PHILOSOPHY

- Cryptography provides integrity, not truth.
- Machine learning provides inference, not certainty.
- Security is cost-increasing, not absolute.
- All outputs are probabilistic.
- All components must be replaceable.

---

## 4. THREAT MODEL (INITIAL)

Assume adversary can:

- Use frontier LLMs
- Paraphrase outputs
- Lightly edit text
- Prompt for stylistic variation

Assume adversary cannot:

- Modify VATA model weights
- Modify scoring code without changing hashes
- Falsify local execution environment without detection

---

## 5. CLAIMS WE CAN MAKE

- A specific model produced a specific score
- The model artifact hash matches a published hash
- The scoring code hash matches a published hash
- The computation was reproducible

---

## 6. CLAIMS WE WILL NOT MAKE

- Content is human
- Content is AI
- Content origin is known
- Content intent is known

---

## 7. TERMINOLOGY

Score:
    A floating point probability in [0,1]

Engine:
    A locally executable forensic scoring system

Manifest:
    A JSON document binding model hash, code hash, and outputs

Artifact:
    Any file produced by the engine

---

## 8. RELEASE DISCIPLINE

- Every release has a version number
- Every release has a changelog
- No breaking changes without version bump

---

## 9. DESIGN CONSTRAINTS

- Local-first execution
- Deterministic where possible
- Reproducible results
- Minimal external dependencies

---

## 10. GUIDING PRINCIPLE

If a claim cannot survive hostile technical scrutiny, it is not allowed.
