import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--compute-only', action='store_true')
args, _ = parser.parse_known_args()
import os
from pathlib import Path

from web3 import Web3
from eth_account import Account

RPC = os.getenv("RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com")
CONTRACT = os.getenv("ANCHOR_CONTRACT", "").strip()  # required
PRIVATE_KEY = os.getenv("DEPLOYER_PRIVATE_KEY", "").strip()  # required

MERKLE_FILE = Path("swarm_openai_merkle.json")
RECEIPT_FILE = Path("anchor_receipt.json")

def build_fees(w3: Web3):
    tip = w3.to_wei(1, "gwei")
    try:
        block = w3.eth.get_block("latest")
        base_fee = block.get("baseFeePerGas")
        if base_fee is None:
            raise ValueError("no baseFeePerGas")
        max_fee = int(base_fee * 2 + tip)
        if max_fee < tip:
            max_fee = tip + w3.to_wei(2, "gwei")
        return tip, max_fee
    except Exception:
        gp = w3.eth.gas_price
        max_fee = int(gp + w3.to_wei(2, "gwei"))
        if max_fee < tip:
            max_fee = tip + w3.to_wei(2, "gwei")
        return tip, max_fee

def main():
    if not CONTRACT:
        raise SystemExit("Missing env var ANCHOR_CONTRACT (set it to your deployed contract address).")
    if not PRIVATE_KEY:
        raise SystemExit("Missing env var DEPLOYER_PRIVATE_KEY (set it for this session only).")
    if not MERKLE_FILE.exists():
        raise SystemExit("Missing swarm_openai_merkle.json. Click 'Build CSV + Hashes + Merkle root' first.")

    merkle_doc = json.loads(MERKLE_FILE.read_text(encoding="utf-8"))
    root = (merkle_doc.get("merkle_root_sha256_hex") or "").strip()
    if not root or len(root) != 64:
        raise SystemExit("Merkle root missing/invalid in swarm_openai_merkle.json (expected 64 hex chars).")

    root_hex = "0x" + root

    # Compute-only mode: print root and exit (no tx)
    if args.compute_only:
        print(json.dumps({
            "ok": True,
            "contract": CONTRACT,
            "merkle_root": root_hex,
            "compute_only": True,
        }))
        return    # COMPUTE ONLY MODE (no transaction)
    if os.environ.get("COMPUTE_ONLY") == "1":
        print(json.dumps({
            "ok": True,
            "contract": CONTRACT,
            "merkle_root": root_hex,
            "compute_only": True
        }))
        return

    w3 = Web3(Web3.HTTPProvider(RPC))
    if not w3.is_connected():
        raise SystemExit(f"RPC connection failed: {RPC}")

    acct = Account.from_key(PRIVATE_KEY)
    sender = acct.address
    chain_id = w3.eth.chain_id

    # Minimal ABI for your MerkleAnchor contract
    abi = [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "bytes32", "name": "root", "type": "bytes32"},
                {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
                {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
            ],
            "name": "Anchored",
            "type": "event",
        },
        {"inputs": [{"internalType": "bytes32", "name": "root", "type": "bytes32"}], "name": "anchor", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    ]

    c = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT), abi=abi)

    nonce = w3.eth.get_transaction_count(sender)
    tx = c.functions.anchor(bytes.fromhex(root)).build_transaction(
        {"from": sender, "nonce": nonce, "chainId": chain_id}
    )

    tx["gas"] = int(w3.eth.estimate_gas(tx) * 1.2)
    tip, max_fee = build_fees(w3)
    tx["maxPriorityFeePerGas"] = tip
    tx["maxFeePerGas"] = max_fee

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction).hex()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Update/append local receipt file
    if RECEIPT_FILE.exists():
        data = json.loads(RECEIPT_FILE.read_text(encoding="utf-8"))
    else:
        data = {"network": "sepolia"}

    data["contract"] = CONTRACT
    data["merkle_root"] = root_hex
    data.setdefault("anchor_txs", [])
    if tx_hash not in data["anchor_txs"]:
        data["anchor_txs"].append(tx_hash)

    RECEIPT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "contract": CONTRACT,
        "merkle_root": root_hex,
        "tx": tx_hash,
        "blockNumber": receipt.get("blockNumber"),
        "receipt_file": str(RECEIPT_FILE),
    }))

if __name__ == "__main__":
    main()



