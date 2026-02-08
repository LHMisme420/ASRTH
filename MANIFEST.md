# Provenance Manifest (Sepolia)

Contract:
0x834AA2587c311E773851ecBB1cDC4eFAaA98c740

Anchored Merkle root:
0xe02ea3dcbfb339f25f086cad160827149274422d581965102aaed063ca814775

Transactions:
- 0x2f5f15c60082b3a51ac0466fc3d2c6a6e984a80e5d11b7bab7aeff032d9e06ee
- 0x844c187fbde5346ba86f18d586c353fe538c5657e03bef209daf3de867da4b8d

Verify (on-chain root):
powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_anchor.ps1

Verify (end-to-end, local == on-chain):
powershell -ExecutionPolicy Bypass -File .\proof_bundle\verify_full.ps1
