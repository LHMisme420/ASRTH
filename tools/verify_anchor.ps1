
# ---- fetch tx input with retries (public RPC indexing lag) ----
$inp = $null
for ($i=1; $i -le 12; $i++) {
  try {
    $line = (cast tx $tx --rpc-url $env:RPC 2>$null | Select-String -Pattern "input" | ForEach-Object { $_.ToString().Trim() })
    if ($line) {
      $parts = $line -split "input\s+"
      $inp = $parts[-1].Trim().ToLowerInvariant()
      break
    }
  } catch {}
  Start-Sleep -Seconds 5
}

if (-not $inp) {
  throw "Could not read tx input after retries. RPC may be lagging. Try again in 1 minute: powershell -ExecutionPolicy Bypass -File tools/verify_anchor.ps1"
}

if ($inp -ne ("0x" + $expected)) {
  Write-Host "❌ On-chain input does not match manifest hash" -ForegroundColor Red
  Write-Host "Tx input:  $inp"
  Write-Host "Expected:  0x$expected"
  exit 1
}

Write-Host "✅ On-chain anchor verified (tx input matches hash)"
