import json, hashlib, sys

def sha256_hex(a_hex: str, b_hex: str) -> str:
    return hashlib.sha256(bytes.fromhex(a_hex) + bytes.fromhex(b_hex)).hexdigest()

def verify(leaf_hex, proof_list, root_hex, index):
    cur = leaf_hex
    idx = index
    for sib in proof_list:
        if idx % 2 == 0:
            cur = sha256_hex(cur, sib)
        else:
            cur = sha256_hex(sib, cur)
        idx //= 2
    return cur == root_hex

if len(sys.argv) != 2:
    print("Usage: python verify_inclusion.py proofs/<id>.json")
    sys.exit(1)

p = json.load(open(sys.argv[1], "r", encoding="utf-8"))
leaf = p["leaf_sha256_hex"]
proof = p["proof_sha256_hex"]
root = p["root_sha256_hex"]
idx = int(p["leaf_index"])

ok = verify(leaf, proof, root, idx)
print("VALID" if ok else "INVALID")
