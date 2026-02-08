param(
  [string]$RPC = "https://ethereum-sepolia-rpc.publicnode.com",
  [string]$TX  = "0x844c187fbde5346ba86f18d586c353fe538c5657e03bef209daf3de867da4b8d",
  [string]$CONTRACT = "0x834AA2587c311E773851ecBB1cDC4eFAaA98c740"
)

$env:ANCHOR_CONTRACT = $CONTRACT

Write-Host "RPC      = $RPC"
Write-Host "CONTRACT = $CONTRACT"
Write-Host "TX       = $TX"

# On-chain root from receipt log topic1
$onchain = (((cast receipt $TX --rpc-url $RPC --json) | ConvertFrom-Json).logs[0].topics[1]).ToLower()
Write-Host "`nOn-chain merkle root:"
Write-Host $onchain

# Local root from your pipeline (no need to anchor; we just read the root it computes)
$localJson = python .\anchor_root_only.py | ConvertFrom-Json
$local = ($localJson.merkle_root).ToLower()

Write-Host "`nLocal recomputed merkle root:"
Write-Host $local

if ($local -eq $onchain) {
  Write-Host "`n✅ VERIFIED: local root matches on-chain root"
  exit 0
} else {
  Write-Host "`n❌ FAILED: local root does NOT match on-chain root"
  exit 2
}

