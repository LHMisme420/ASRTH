param(
  [Parameter(Mandatory=$true)][string]$InputPath
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$art  = Join-Path $root "artifacts"
New-Item -ItemType Directory -Force -Path $art | Out-Null

$inputFile = Join-Path $root "input.txt"
Copy-Item $InputPath $inputFile -Force

function Sha256($p){ (Get-FileHash $p -Algorithm SHA256).Hash.ToLower() }

$engineVersion="0.1.0"
$schemaVersion="0.1"
$utc=(Get-Date).ToUniversalTime().ToString("o")

$model="fusionnet_nolf.pkl"
$scorer="score.py"

$inHash=Sha256 $inputFile
$modelHash=Sha256 (Join-Path $root $model)
$scorerHash=Sha256 (Join-Path $root $scorer)

$score = Get-Content $inputFile -Raw | python (Join-Path $root $scorer)
$score=[double]$score.Trim()

$threshold=0.55
$label= if($score -ge $threshold){"human"} else {"ai"}

$features=@{
 schema_version=$schemaVersion
 engine_version=$engineVersion
 input_sha256=$inHash
 features=@{placeholder=1}
} | ConvertTo-Json -Depth 5

$featuresPath=Join-Path $art "features.json"
$features | Set-Content -Encoding utf8 $featuresPath

$scoreObj=@{
 schema_version=$schemaVersion
 engine_version=$engineVersion
 model_sha256=$modelHash
 scorer_sha256=$scorerHash
 score=$score
 label=$label
 threshold=$threshold
} | ConvertTo-Json -Depth 5

$scorePath=Join-Path $art "score.json"
$scoreObj | Set-Content -Encoding utf8 $scorePath

$manifest=@{
 schema_version=$schemaVersion
 engine_version=$engineVersion
 timestamp_utc=$utc
 inputs=@{ "input.txt"=$inHash }
 artifacts=@{
   "features.json"=Sha256 $featuresPath
   "score.json"=Sha256 $scorePath
 }
 code=@{
   scorer_file=$scorer
   scorer_sha256=$scorerHash
 }
 model=@{
   model_file=$model
   model_sha256=$modelHash
 }
} | ConvertTo-Json -Depth 6

$manifestPath=Join-Path $art "manifest.json"
$manifest | Set-Content -Encoding utf8 $manifestPath

$hashes=@()
$hashes+= "$(Sha256 $inputFile)  input.txt"
$hashes+= "$(Sha256 $featuresPath)  artifacts/features.json"
$hashes+= "$(Sha256 $scorePath)  artifacts/score.json"
$hashes+= "$(Sha256 $manifestPath)  artifacts/manifest.json"
$hashes+= "$scorerHash  $scorer"
$hashes+= "$modelHash  $model"
$hashes | Set-Content -Encoding utf8 (Join-Path $art "hashes.txt")

Write-Output "OK"
Write-Output "score=$score"
Write-Output "label=$label"
