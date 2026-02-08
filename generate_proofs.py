import json, hashlib, os

HASHES_FILE = "swarm_openai_hashes.jsonl"
MERKLE_META = "swarm_openai_merkle.json"
OUT_DIR = "proofs"

def sha256_hex(a_hex: str, b_hex: str) -> str:
    return hashlib.sha256(bytes.fromhex(a_hex) + bytes.fromhex(b_hex)).hexdigest()

def load_leaves():
    leaves = []
    with open(HASHES_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            # Try common keys
            h = (obj.get("sha256") or obj.get("hash") or obj.get("leaf") or obj.get("leaf_sha256") or "").strip().lower()
            if h.startswith("0x"):
                h = h[2:]
            if len(h) != 64:
                raise SystemExit(f"Bad hash at line {i+1}: expected 64 hex chars, got: {h}")

            # Pick an id (best effort)
            _id = str(obj.get("id") or obj.get("name") or obj.get("file") or obj.get("key") or i)
            # sanitize filename
            _id = "".join(c if c.isalnum() or c in ("-", "_", ".", "@") else "_" for c in _id)

            leaves.append({"id": _id, "hash": h})

    if not leaves:
        raise SystemExit("No leaves loaded from swarm_openai_hashes.jsonl")
    return leaves

def build_levels(leaf_hashes):
    levels = [leaf_hashes]
    level = leaf_hashes[:]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            nxt.append(sha256_hex(left, right))
        levels.append(nxt)
        level = nxt
    return levels

def merkle_proof(levels, index):
    proof = []
    idx = index
    for level in levels[:-1]:
        pair = idx ^ 1
        if pair < len(level):
            proof.append(level[pair])
        else:
            proof.append(level[idx])  # duplicated last
        idx //= 2
    return proof

def main():
    leaves = load_leaves()
    leaf_hashes = [x["hash"] for x in leaves]
    levels = build_levels(leaf_hashes)
    root = levels[-1][0]

    # Optional: compare against meta root if present
    meta = json.load(open(MERKLE_META, "r", encoding="utf-8"))
    expected = (meta.get("merkle_root_sha256_hex") or "").strip().lower()
    if expected and expected != root:
        raise SystemExit(f"Root mismatch! computed={root} expected={expected}")

    os.makedirs(OUT_DIR, exist_ok=True)

    for i, leaf in enumerate(leaves):
        out = {
            "id": leaf["id"],
            "leaf_sha256_hex": leaf["hash"],
            "proof_sha256_hex": merkle_proof(levels, i),
            "root_sha256_hex": root,
            "leaf_index": i,
            "leaf_count": len(leaves),
            "hash_function": "sha256",
            "pair_rule": "sha256(left||right)",
            "odd_rule": "duplicate_last",
        }
        with open(os.path.join(OUT_DIR, f"{leaf['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

    print(f"OK: generated {len(leaves)} inclusion proofs in ./{OUT_DIR}")
    print(f"root_sha256_hex={root}")

if __name__ == "__main__":
    main()
