param(
    [string]$WorkspaceRoot = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
}

$sourceJson = Join-Path $WorkspaceRoot "source\Game.en.json"
$translationNestedJson = Join-Path $WorkspaceRoot "source\Game.tr.nested.json"
$workingJson = Join-Path $WorkspaceRoot "working\Game.tr.json"
$workingCsv = Join-Path $WorkspaceRoot "working\Game.tr.csv"
$importScript = Join-Path $WorkspaceRoot "tools\import_nested_json.py"
$ioScript = Join-Path $WorkspaceRoot "tools\translation_io.py"

python $importScript --source $sourceJson --translation $translationNestedJson --output $workingJson
if ($LASTEXITCODE -ne 0) {
    throw "Nested JSON import failed with exit code $LASTEXITCODE"
}

python $ioScript json-to-csv --input $workingJson --output $workingCsv
if ($LASTEXITCODE -ne 0) {
    throw "JSON to CSV conversion failed with exit code $LASTEXITCODE"
}

Write-Host "Refreshed Turkish working files:"
Write-Host " - $workingJson"
Write-Host " - $workingCsv"
