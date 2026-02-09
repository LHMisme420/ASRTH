# tools/verify_manifest.ps1
# Verifies manifest hash lock

$ErrorActionPreference = "Stop"

$repoRoot = (git rev-parse --show-toplevel)
if (-not $repoRoot) { throw "Not in a git repo" }

$manifestPath = Join-Path $repoRoot "vata\artifacts\manifest.json"
$hashPath     = Join-Path $repoRoot "vata\artifacts\manifest_hash.txt"

if (!(Test-Path $manifestPath)) { throw "Missing $manifestPath" }
if (!(Test-Path $hashPath))     { throw "Missing manifest_hash.txt (run lock script)" }

$expected = (Get-Content -Raw $hashPath).Trim().ToLowerInvariant()

$canonical = python -c @"
import json,sys
with open(r'$manifestPath','rb') as f:
    data = f.read().decode('utf-8-sig')  # strips UTF-8 BOM if present
    obj = json.loads(data)
print(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False), end='')
"@

$bytes = [System.Text.Encoding]::UTF8.GetBytes($canonical)
$sha   = [System.Security.Cryptography.SHA256]::Create()
$actual = ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""

if ($actual -ne $expected) {
  Write-Host "❌ MANIFEST HASH MISMATCH" -ForegroundColor Red
  Write-Host "Expected: $expected"
  Write-Host "Actual:   $actual"
  exit 1
}

Write-Host "✅ Manifest verified"
