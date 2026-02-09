# tools/verify_anchor.ps1
# Verifies:
# 1) manifest_hash.txt matches canonical manifest.json
# 2) manifest_anchor_tx.txt exists and tx input contains the hash

$ErrorActionPreference = "Stop"

$repoRoot = (git rev-parse --show-toplevel)
if (-not $repoRoot) { throw "Not in a git repo" }

$manifestPath = Join-Path $repoRoot "vata\artifacts\manifest.json"
$hashPath     = Join-Path $repoRoot "vata\artifacts\manifest_hash.txt"
$txPath       = Join-Path $repoRoot "vata\artifacts\manifest_anchor_tx.txt"

if (-not $env:RPC) { throw "Set RPC first: `$env:RPC='https://ethereum-sepolia-rpc.publicnode.com'" }

# ---- verify local hash first (reuse BOM-safe canonicalization) ----
if (!(Test-Path $manifestPath)) { throw "Missing $manifestPath" }
if (!(Test-Path $hashPath))     { throw "Missing $hashPath" }

$expected = (Get-Content -Raw $hashPath).Trim().ToLowerInvariant()

$canonical = python -c @"
import json,sys
with open(r'$manifestPath','rb') as f:
    data=f.read().decode('utf-8-sig')
    obj=json.loads(data)
print(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False), end='')
"@

$bytes = [System.Text.Encoding]::UTF8.GetBytes($canonical)
$sha   = [System.Security.Cryptography.SHA256]::Create()
$actual = ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""

if ($actual -ne $expected) {
  Write-Host "❌ Local manifest hash mismatch" -ForegroundColor Red
  Write-Host "Expected: $expected"
  Write-Host "Actual:   $actual"
  exit 1
}

Write-Host "✅ Local manifest hash verified"

# ---- verify on-chain anchor ----
if (!(Test-Path $txPath)) { throw "Missing $txPath (write the tx hash there)" }

$tx = (Get-Content -Raw $txPath).Trim()
if ($tx -notmatch '^0x[0-9a-fA-F]{64}$') { throw "Invalid tx hash in manifest_anchor_tx.txt" }

$input = (cast tx $tx --rpc-url $env:RPC | Select-String -Pattern "input" | ForEach-Object { $_.ToString().Trim() })
if (-not $input) { throw "Could not read tx input. Is RPC working?" }

# input line looks like: "input: 0x...."
$parts = $input -split "input:\s+"
$inp = $parts[-1].Trim().ToLowerInvariant()

if ($inp -ne ("0x" + $expected)) {
  Write-Host "❌ On-chain input does not match manifest hash" -ForegroundColor Red
  Write-Host "Tx input:  $inp"
  Write-Host "Expected:  0x$expected"
  exit 1
}

Write-Host "✅ On-chain anchor verified (tx input matches hash)"
