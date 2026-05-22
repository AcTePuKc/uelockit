param(
    [ValidateSet("auto", "csv", "json")]
    [string]$TranslationFormat = "auto",
    [string]$WorkspaceRoot = "",
    [string]$ConfigPath = "",
    [string]$LocalizationTargetName = "Game",
    [string]$CultureTag = "bg",
    [string]$SourceLocresPath = "",
    [string]$TranslationCsvPath = "",
    [string]$TranslationJsonPath = "",
    [string]$OutputLocresPath = "",
    [string]$UnrealLocresPath = "",
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Split-Path -Parent $PSCommandPath
}

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $defaultConfigPath = Join-Path $WorkspaceRoot "config\UELocKit.config.psd1"
    if (Test-Path -LiteralPath $defaultConfigPath) {
        $ConfigPath = $defaultConfigPath
    }
}

$config = $null
if (-not [string]::IsNullOrWhiteSpace($ConfigPath)) {
    if (-not (Test-Path -LiteralPath $ConfigPath)) {
        throw "Config file not found: $ConfigPath"
    }
    $config = Import-PowerShellDataFile -LiteralPath $ConfigPath
}

function Resolve-FirstExistingPath {
    param(
        [string[]]$Candidates
    )

    foreach ($candidate in $Candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    return $null
}

function Get-ConfigValue {
    param(
        [hashtable]$Config,
        [string]$Name
    )

    if ($null -ne $Config -and $Config.ContainsKey($Name)) {
        return [string]$Config[$Name]
    }

    return ""
}

function Resolve-WorkspacePath {
    param(
        [string]$PathValue,
        [string]$BasePath
    )

    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return ""
    }

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PathValue)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $PathValue))
}

if ($LocalizationTargetName -eq "Game") {
    $configValue = Get-ConfigValue -Config $config -Name "LocalizationTargetName"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $LocalizationTargetName = $configValue
    }
}
if ($CultureTag -eq "bg") {
    $configValue = Get-ConfigValue -Config $config -Name "CultureTag"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $CultureTag = $configValue
    }
}
if ([string]::IsNullOrWhiteSpace($PythonExe) -or $PythonExe -eq "python") {
    $configValue = Get-ConfigValue -Config $config -Name "PythonExe"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $PythonExe = $configValue
    }
}

if ([string]::IsNullOrWhiteSpace($SourceLocresPath)) {
    $configValue = Get-ConfigValue -Config $config -Name "SourceLocresPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $SourceLocresPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
    else {
        $SourceLocresPath = Join-Path $WorkspaceRoot ("source\{0}.en.locres" -f $LocalizationTargetName)
    }
}
else {
    $SourceLocresPath = Resolve-WorkspacePath -PathValue $SourceLocresPath -BasePath $WorkspaceRoot
}
if ([string]::IsNullOrWhiteSpace($TranslationCsvPath)) {
    $configValue = Get-ConfigValue -Config $config -Name "TranslationCsvPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $TranslationCsvPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
    else {
        $TranslationCsvPath = Join-Path $WorkspaceRoot ("working\{0}.{1}.csv" -f $LocalizationTargetName, $CultureTag)
    }
}
else {
    $TranslationCsvPath = Resolve-WorkspacePath -PathValue $TranslationCsvPath -BasePath $WorkspaceRoot
}
if ([string]::IsNullOrWhiteSpace($TranslationJsonPath)) {
    $configValue = Get-ConfigValue -Config $config -Name "TranslationJsonPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $TranslationJsonPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
    else {
        $TranslationJsonPath = Join-Path $WorkspaceRoot ("working\{0}.{1}.json" -f $LocalizationTargetName, $CultureTag)
    }
}
else {
    $TranslationJsonPath = Resolve-WorkspacePath -PathValue $TranslationJsonPath -BasePath $WorkspaceRoot
}
if ([string]::IsNullOrWhiteSpace($OutputLocresPath)) {
    $configValue = Get-ConfigValue -Config $config -Name "OutputLocresPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $OutputLocresPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
    else {
        $OutputLocresPath = Join-Path $WorkspaceRoot ("output\{0}.{1}.locres" -f $LocalizationTargetName, $CultureTag)
    }
}
else {
    $OutputLocresPath = Resolve-WorkspacePath -PathValue $OutputLocresPath -BasePath $WorkspaceRoot
}

if ([string]::IsNullOrWhiteSpace($UnrealLocresPath)) {
    $UnrealLocresPath = Resolve-FirstExistingPath @(
        (Get-ConfigValue -Config $config -Name "UnrealLocresPath"),
        $env:UNREALLOCRES_EXE,
        (Join-Path $WorkspaceRoot "tools\UnrealLocres.exe"),
        "C:\MyGames\Locres Studio\UnrealLocres.exe"
    )
}

$outputDir = Split-Path -Parent $OutputLocresPath
$runId = [System.Guid]::NewGuid().ToString("N")
$tempCsv = Join-Path $outputDir ("{0}.{1}.from-json.tmp.csv" -f [System.IO.Path]::GetFileNameWithoutExtension($OutputLocresPath), $runId)
$tempLocres = Join-Path $outputDir ("{0}.{1}.tmp{2}" -f [System.IO.Path]::GetFileNameWithoutExtension($OutputLocresPath), $runId, [System.IO.Path]::GetExtension($OutputLocresPath))
$converterScript = Join-Path $WorkspaceRoot "tools\translation_io.py"

function Wait-FileReady {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [int]$TimeoutMs = 5000
    )

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while ($sw.ElapsedMilliseconds -lt $TimeoutMs) {
        try {
            $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
            $stream.Dispose()
            return
        }
        catch {
            Start-Sleep -Milliseconds 200
        }
    }

    throw "Timed out waiting for file lock to clear: $Path"
}

if (-not $UnrealLocresPath) {
    throw "Could not locate UnrealLocres.exe. Pass -UnrealLocresPath or set UNREALLOCRES_EXE."
}
if (-not (Test-Path -LiteralPath $UnrealLocresPath)) {
    throw "UnrealLocres.exe not found at: $UnrealLocresPath"
}
if (-not (Test-Path -LiteralPath $SourceLocresPath)) {
    throw "Source locres not found: $SourceLocresPath"
}
if (-not (Test-Path -LiteralPath $converterScript)) {
    throw "Missing translation converter script: $converterScript"
}

$resolvedFormat = $TranslationFormat
if ($resolvedFormat -eq "auto") {
    if (Test-Path -LiteralPath $TranslationJsonPath) {
        $resolvedFormat = "json"
    }
    elseif (Test-Path -LiteralPath $TranslationCsvPath) {
        $resolvedFormat = "csv"
    }
    else {
        throw "No translation source found. Expected one of:`n - $TranslationJsonPath`n - $TranslationCsvPath"
    }
}

New-Item -ItemType Directory -Force $outputDir | Out-Null

$inputCsvPath = $TranslationCsvPath
switch ($resolvedFormat) {
    "json" {
        if (-not (Test-Path -LiteralPath $TranslationJsonPath)) {
            throw "Translation JSON not found: $TranslationJsonPath"
        }
        & $PythonExe $converterScript json-to-csv --input $TranslationJsonPath --output $tempCsv
        if ($LASTEXITCODE -ne 0) {
            throw "JSON to CSV conversion failed with exit code $LASTEXITCODE"
        }
        $inputCsvPath = $tempCsv
    }
    "csv" {
        if (-not (Test-Path -LiteralPath $TranslationCsvPath)) {
            throw "Translation CSV not found: $TranslationCsvPath"
        }
    }
}

if (Test-Path -LiteralPath $tempLocres) {
    Remove-Item -LiteralPath $tempLocres -Force
}

& $UnrealLocresPath import -f csv $SourceLocresPath $inputCsvPath -o $tempLocres
if ($LASTEXITCODE -ne 0) {
    throw "UnrealLocres import failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath $tempLocres)) {
    throw "Expected UnrealLocres output was not created: $tempLocres"
}

Wait-FileReady -Path $tempLocres
Copy-Item -LiteralPath $tempLocres -Destination $OutputLocresPath -Force

if (Test-Path -LiteralPath $tempCsv) {
    Remove-Item -LiteralPath $tempCsv -Force
}
if (Test-Path -LiteralPath $tempLocres) {
    Remove-Item -LiteralPath $tempLocres -Force
}

Write-Host ("Built locres from {0}: {1}" -f $resolvedFormat, $OutputLocresPath)
