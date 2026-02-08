# Manifest

This snapshot produces Merkle root:

0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775

Inputs:
- swarm_openai_merkle.json
- vata/artifacts/manifest.json
- vata/artifacts/hashes.txt

Root is computed by:
anchor_root_only.py

Verification:
powershell -ExecutionPolicy Bypass -File proof_bundle\verify_full.ps1
