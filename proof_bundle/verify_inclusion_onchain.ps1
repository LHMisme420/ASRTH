param(
  [Parameter(Mandatory=$true)][string]$Proof,
  [string]$RPC = "https://ethereum-sepolia-rpc.publicnode.com",
  [string]$TX  = "0x844c187fbde5346ba86f18d586c353fe538c5657e03bef209daf3de867da4b8d"
)

if (!(Test-Path $Proof)) { throw "Proof file not found: $Proof" }

Write-Host "RPC  = $RPC"
Write-Host "TX   = $TX"
Write-Host "PROOF= $Proof"

# 1) Pull on-chain root from receipt log topic1
$onchain = (((cast receipt $TX --rpc-url $RPC --json) | ConvertFrom-Json).logs[0].topics[1]).ToLower()
Write-Host "`nOn-chain root:"
Write-Host $onchain

# 2) Read proof JSON root
$p = Get-Content $Proof -Raw | ConvertFrom-Json
$proofRoot = ("0x" + $p.root_sha256_hex.Trim().ToLower().Replace("0x",""))
Write-Host "`nProof file root:"
Write-Host $proofRoot

if ($proofRoot -ne $onchain) {
  Write-Host "`n❌ FAILED: proof root != on-chain root"
  exit 2
}

# 3) Run python verifier
Write-Host "`nRunning inclusion verification..."
$py = python .\verify_inclusion.py $Proof
Write-Host $py

if ($py -match "VALID") {
  Write-Host "`n✅ VERIFIED: proof is valid AND matches on-chain root"
  exit 0
} else {
  Write-Host "`n❌ FAILED: proof did not verify"
  exit 3
}
