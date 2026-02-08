param(
  [string]$RPC = "https://ethereum-sepolia-rpc.publicnode.com",
  [string]$TX  = "0x2f5f15c60082b3a51ac0466fc3d2c6a6e984a80e5d11b7bab7aeff032d9e06ee"
)

Write-Host "RPC = $RPC"
Write-Host "TX  = $TX"

$root = (((cast receipt $TX --rpc-url $RPC --json) | ConvertFrom-Json).logs[0].topics[1])
Write-Host "Anchored merkle root (from receipt log):"
Write-Host $root
