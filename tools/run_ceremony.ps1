param(
  [switch]$CommitPush
)

$ErrorActionPreference = "Stop"

function Require-Command($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Missing required command: $name"
  }
}

Require-Command git
Require-Command python
Require-Command cast

$repoRoot = (git rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) { throw "Not inside a git repo. cd into the ASRTH repo and try again." }

Set-Location $repoRoot

if (-not $env:RPC) { throw "RPC not set. Example: `$env:RPC='https://ethereum-sepolia-rpc.publicnode.com'" }
if (-not $env:DEPLOYER_PRIVATE_KEY) { throw "DEPLOYER_PRIVATE_KEY not set." }

$hashPath = Join-Path $repoRoot "vata\artifacts\manifest_hash.txt"
$txPath   = Join-Path $repoRoot "vata\artifacts\manifest_anchor_tx.txt"

Write-Host ""
Write-Host "== VATA Ceremony ==" -ForegroundColor Cyan
Write-Host "Repo: $repoRoot"
Write-Host "RPC:  $($env:RPC)"
Write-Host ""

Write-Host "[1/5] Locking manifest hash..." -ForegroundColor Yellow
powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\lock_manifest.ps1") | Out-Host

Write-Host "[2/5] Verifying local manifest hash..." -ForegroundColor Yellow
powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\verify_manifest.ps1") | Out-Host

$hash = (Get-Content -Raw $hashPath).Trim().ToLowerInvariant()
if ($hash.Length -ne 64 -or $hash -notmatch '^[0-9a-f]{64}$') { throw "Invalid hash in $hashPath" }

Write-Host "[3/5] Anchoring on-chain (tx-to-self calldata)..." -ForegroundColor Yellow
$to = (cast wallet address --private-key $env:DEPLOYER_PRIVATE_KEY).Trim()
Write-Host "To:   $to"
Write-Host "Data: 0x$hash"

$out = cast send $to 0x$hash --rpc-url $env:RPC --private-key $env:DEPLOYER_PRIVATE_KEY --value 0
$outText = ($out | Out-String)
$tx = ([regex]::Match($outText, "0x[a-fA-F0-9]{64}")).Value
if (-not $tx) { throw "Could not parse tx hash from cast output:`n$outText" }

Write-Host "Tx:   $tx" -ForegroundColor Green

Write-Host "[4/5] Writing anchor tx file..." -ForegroundColor Yellow
Set-Content -NoNewline -Encoding ASCII $txPath $tx
Write-Host "Saved: $txPath" -ForegroundColor Green

Write-Host "[5/5] Verifying on-chain anchor..." -ForegroundColor Yellow
powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\verify_anchor.ps1") | Out-Host

Write-Host ""
Write-Host "✅ Ceremony complete." -ForegroundColor Green
Write-Host "Hash: $hash"
Write-Host "Tx:   $tx"
Write-Host ""

if ($CommitPush) {
  Write-Host "Committing & pushing ceremony outputs..." -ForegroundColor Cyan
  git add $hashPath $txPath tools\lock_manifest.ps1 tools\verify_manifest.ps1 tools\verify_anchor.ps1 | Out-Null
  $staged = git diff --cached --name-only
  if ($staged) {
    git commit -m "Ceremony: lock + anchor manifest hash" | Out-Host
    git push origin main | Out-Host
    Write-Host "✅ Pushed." -ForegroundColor Green
  } else {
    Write-Host "Nothing to commit." -ForegroundColor DarkYellow
  }
}
