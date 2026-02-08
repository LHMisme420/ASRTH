# VATA-Forensics

**VATA-Forensics** is a lightweight, reproducible safety-evaluation harness for
testing AI systems under adversarial conditions with a cryptographic-style
provenance mindset.

It combines:

- A **Guardian Gate** (pre-model PII filter)
- A **Swarm Harness** (interactive prompt loop)
- **Structured Logging** (JSONL)
- **Scoring & Categorization** (model vs infrastructure failures)
- **CSV + Summary Export**

The goal is to produce *verifiable, auditable evidence* of model behavior,
rather than screenshots or anecdotal claims.

---

## Architecture

## On-chain provenance proof (Sepolia)

This repo anchors a Merkle root to an on-chain MerkleAnchor contract and provides scripts to verify:

- Verify the on-chain anchored root:
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1

- Verify local snapshot matches the on-chain root (end-to-end):
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_full.ps1

## On-chain provenance proof (Sepolia)

This repo produces a deterministic Merkle root for the current snapshot and anchors it on-chain.

- Contract: 0x834AA2587c311E773851ecBB1cDC4eFAaA98c740
- Merkle root: 0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775
- Transactions:
  - 0x2f5f15c60082b3a51ac0466fc3d2c6a6e984a80e5d11b7bab7aeff032d9e06ee
  - 0x844c187fbde5346ba86f18d586c353fe538c5657e03bef209daf3de867da4b8d

### Verify
- On-chain root:
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1

- End-to-end (local snapshot matches on-chain):
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_full.ps1

## On-chain Provenance Proof (Sepolia)

This repository produces a deterministic Merkle root for its current snapshot and anchors it on-chain.

Contract:
0x834AA2587c311E773851ecBB1cDC4eFAaA98c740

Merkle Root:
0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775

Verify:
- On-chain root:
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1
- End-to-end:
  powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_full.ps1

## Verify inclusion of a single record

1) Generate proofs (or use the committed ./proofs folder):
   python .\generate_proofs.py

2) Verify any proof file:
   python .\verify_inclusion.py .\proofs\0.json

Expected output: VALID

This verifies membership against the Merkle root:
0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775

On-chain verification:
powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1

## Verify inclusion of a single record (Merkle proof)

This repo can generate Merkle inclusion proofs for individual record-hashes that belong to the anchored snapshot.

Anchored Merkle root (Sepolia):
0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775

### Generate proofs
python .\generate_proofs.py

### Verify a proof
python .\verify_inclusion.py .\proofs\0.json

Expected output: VALID

### Verify the root is anchored on-chain
powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1
