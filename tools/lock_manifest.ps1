# tools/lock_manifest.ps1
# Locks vata/artifacts/manifest.json by deterministic SHA256

$ErrorActionPreference = "Stop"

$repoRoot = (git rev-parse --show-toplevel)
if (-not $repoRoot) { throw "Not in a git repo" }

$manifestPath = Join-Path $repoRoot "vata\artifacts\manifest.json"
$hashPath     = Join-Path $repoRoot "vata\artifacts\manifest_hash.txt"

if (!(Test-Path $manifestPath)) {
  throw "Missing $manifestPath"
}

$canonical = python -c @"
import json,sys
with open(r'$manifestPath','rb') as f:
    data = f.read().decode('utf-8-sig')  # strips UTF-8 BOM if present
    obj = json.loads(data)
print(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False), end='')
"@


$bytes = [System.Text.Encoding]::UTF8.GetBytes($canonical)
$sha   = [System.Security.Cryptography.SHA256]::Create()
$hash  = ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""

Set-Content -NoNewline -Encoding ASCII $hashPath $hash
Write-Host "Manifest locked:"
Write-Host $hashPath
Write-Host $hash
