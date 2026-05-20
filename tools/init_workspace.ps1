param(
    [string]$WorkspaceRoot = "",
    [string]$SourceLocresPath = "",
    [string]$LocalizationTargetName = "Game",
    [string]$CultureTag = "bg",
    [string]$PythonExe = "python",
    [string]$UnrealLocresPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
}

if ([string]::IsNullOrWhiteSpace($SourceLocresPath)) {
    $SourceLocresPath = Join-Path $WorkspaceRoot ("source\{0}.en.locres" -f $LocalizationTargetName)
}

$scriptPath = Join-Path (Split-Path -Parent $PSCommandPath) "init_workspace.py"

$command = @(
    $scriptPath,
    "--workspace-root", $WorkspaceRoot,
    "--source-locres", $SourceLocresPath,
    "--localization-target", $LocalizationTargetName,
    "--culture-tag", $CultureTag
)

if (-not [string]::IsNullOrWhiteSpace($UnrealLocresPath)) {
    $command += @("--unreal-locres", $UnrealLocresPath)
}

& $PythonExe @command
if ($LASTEXITCODE -ne 0) {
    throw "Workspace initialization failed with exit code $LASTEXITCODE"
}
