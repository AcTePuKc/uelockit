param(
    [string]$PackageName = "Subnautica2-BG_P",
    [string]$CultureFolder = "bg",
    [string]$CultureCode = "bg-BG",
    [ValidateSet("auto", "csv", "json")]
    [string]$TranslationFormat = "auto",
    [string]$WorkspaceRoot = "",
    [string]$ConfigPath = "",
    [string]$GameName = "Subnautica2",
    [string]$LocalizationTargetName = "Game",
    [string]$TranslationCsvPath = "",
    [string]$TranslationJsonPath = "",
    [string]$OutputLocresPath = "",
    [string]$GamePaksDir = "",
    [string]$UnrealPakPath = "",
    [string]$RetocPath = "",
    [bool]$DeployToGame = $true,
    [bool]$CreateZip = $false,
    [string]$ZipPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
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

if ($PackageName -eq "Subnautica2-BG_P") {
    $configValue = Get-ConfigValue -Config $config -Name "PackageName"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $PackageName = $configValue
    }
}
if ($CultureFolder -eq "bg") {
    $configValue = Get-ConfigValue -Config $config -Name "CultureFolder"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $CultureFolder = $configValue
    }
}
if ($CultureCode -eq "bg-BG") {
    $configValue = Get-ConfigValue -Config $config -Name "CultureCode"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $CultureCode = $configValue
    }
}
if ($GameName -eq "Subnautica2") {
    $configValue = Get-ConfigValue -Config $config -Name "GameName"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $GameName = $configValue
    }
}
if ($LocalizationTargetName -eq "Game") {
    $configValue = Get-ConfigValue -Config $config -Name "LocalizationTargetName"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $LocalizationTargetName = $configValue
    }
}

$toolsDir = Join-Path $WorkspaceRoot "tools"
$outputDir = Join-Path $WorkspaceRoot "pak-output"
$stagingRoot = Join-Path $WorkspaceRoot "pak-staging\$PackageName"
$stagingGameLocDir = Join-Path $stagingRoot "$GameName\Content\Localization\Game"
$stagingCultureDir = Join-Path $stagingGameLocDir $CultureFolder
$responseFile = Join-Path $toolsDir "filelist-$PackageName.txt"
$pakOutput = Join-Path $outputDir "$PackageName.pak"
$utocOutput = Join-Path $outputDir "$PackageName.utoc"
$ucasOutput = Join-Path $outputDir "$PackageName.ucas"
$locmetaOutput = Join-Path $outputDir "$LocalizationTargetName.locmeta"
$locresOutput = if ([string]::IsNullOrWhiteSpace($OutputLocresPath)) {
    Join-Path $WorkspaceRoot ("output\{0}.{1}.locres" -f $LocalizationTargetName, $CultureFolder)
}
else {
    $OutputLocresPath
}
$locresBuildScript = Join-Path $WorkspaceRoot "build-locres.ps1"
$zipOutput = if ([string]::IsNullOrWhiteSpace($ZipPath)) {
    Join-Path $outputDir "$PackageName.zip"
}
else {
    $ZipPath
}

if ([string]::IsNullOrWhiteSpace($UnrealPakPath)) {
    $UnrealPakPath = Resolve-FirstExistingPath @(
        (Get-ConfigValue -Config $config -Name "UnrealPakPath"),
        $env:UNREALPAK_EXE,
        (Join-Path $toolsDir "UnrealPak.exe")
    )
}
if ([string]::IsNullOrWhiteSpace($RetocPath)) {
    $RetocPath = Resolve-FirstExistingPath @(
        (Get-ConfigValue -Config $config -Name "RetocPath"),
        $env:RETOC_EXE,
        (Join-Path $toolsDir "retoc\retoc.exe")
    )
}
if ([string]::IsNullOrWhiteSpace($GamePaksDir)) {
    $configValue = Get-ConfigValue -Config $config -Name "GamePaksDir"
    if (-not [string]::IsNullOrWhiteSpace($configValue) -and (Test-Path -LiteralPath $configValue)) {
        $GamePaksDir = $configValue
    }
    else {
        $workspaceParent = Split-Path -Parent $WorkspaceRoot
        $workspaceGrandparent = Split-Path -Parent $workspaceParent
        $candidatePaksDir = Join-Path $workspaceGrandparent "$GameName\Content\Paks"
        if (Test-Path -LiteralPath $candidatePaksDir) {
            $GamePaksDir = $candidatePaksDir
        }
    }
}

if (-not [string]::IsNullOrWhiteSpace($TranslationCsvPath)) {
    $TranslationCsvPath = Resolve-WorkspacePath -PathValue $TranslationCsvPath -BasePath $WorkspaceRoot
}
elseif ($null -ne $config) {
    $configValue = Get-ConfigValue -Config $config -Name "TranslationCsvPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $TranslationCsvPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
}

if (-not [string]::IsNullOrWhiteSpace($TranslationJsonPath)) {
    $TranslationJsonPath = Resolve-WorkspacePath -PathValue $TranslationJsonPath -BasePath $WorkspaceRoot
}
elseif ($null -ne $config) {
    $configValue = Get-ConfigValue -Config $config -Name "TranslationJsonPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $TranslationJsonPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
}

if (-not [string]::IsNullOrWhiteSpace($OutputLocresPath)) {
    $OutputLocresPath = Resolve-WorkspacePath -PathValue $OutputLocresPath -BasePath $WorkspaceRoot
}
elseif ($null -ne $config) {
    $configValue = Get-ConfigValue -Config $config -Name "OutputLocresPath"
    if (-not [string]::IsNullOrWhiteSpace($configValue)) {
        $OutputLocresPath = Resolve-WorkspacePath -PathValue $configValue -BasePath $WorkspaceRoot
    }
}

function Write-UeAsciiString {
    param(
        [System.IO.BinaryWriter]$Writer,
        [string]$Value
    )

    $bytes = [System.Text.Encoding]::ASCII.GetBytes($Value + [char]0)
    $Writer.Write([int]$bytes.Length)
    $Writer.Write($bytes)
}

function New-GameLocmeta {
    param(
        [string]$Path,
        [string]$ExtraCulture
    )

    [byte[]]$magic = 0x4f,0xee,0x4c,0xa1,0x68,0x48,0x55,0x83,0x6c,0x4c,0x46,0xbd,0x70,0xda,0x50,0x7c
    $cultures = @(
        "de-DE",
        "en",
        "es-419",
        "fr-FR",
        "it",
        "ja-JP",
        "ko-KR",
        "pt-BR",
        "ru-RU",
        "uk-UA",
        "zh-Hans",
        $ExtraCulture
    )

    $memory = New-Object System.IO.MemoryStream
    $writer = New-Object System.IO.BinaryWriter($memory)
    try {
        $writer.Write($magic)
        $writer.Write([byte]1)
        Write-UeAsciiString -Writer $writer -Value "en"
        Write-UeAsciiString -Writer $writer -Value "en/Game.locres"
        $writer.Write([uint32]$cultures.Count)
        foreach ($culture in $cultures) {
            Write-UeAsciiString -Writer $writer -Value $culture
        }
        [System.IO.File]::WriteAllBytes($Path, $memory.ToArray())
    }
    finally {
        $writer.Dispose()
        $memory.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $locresBuildScript)) {
    throw "Missing locres build script: $locresBuildScript"
}
if (-not $UnrealPakPath) {
    throw "Could not locate UnrealPak.exe. Pass -UnrealPakPath or set UNREALPAK_EXE."
}
if (-not (Test-Path -LiteralPath $UnrealPakPath)) {
    throw "Missing UnrealPak.exe: $UnrealPakPath"
}
if (-not $RetocPath) {
    throw "Could not locate retoc.exe. Pass -RetocPath or set RETOC_EXE."
}
if (-not (Test-Path -LiteralPath $RetocPath)) {
    throw "Missing retoc.exe: $RetocPath"
}
if ($DeployToGame -and [string]::IsNullOrWhiteSpace($GamePaksDir)) {
    throw "DeployToGame is enabled, but no game Paks directory was found. Pass -GamePaksDir or set -DeployToGame `$false."
}
if ($DeployToGame -and -not (Test-Path -LiteralPath $GamePaksDir)) {
    throw "Missing game Paks dir: $GamePaksDir"
}

& $locresBuildScript `
    -TranslationFormat $TranslationFormat `
    -WorkspaceRoot $WorkspaceRoot `
    -ConfigPath $ConfigPath `
    -LocalizationTargetName $LocalizationTargetName `
    -CultureTag $CultureFolder `
    -TranslationCsvPath $TranslationCsvPath `
    -TranslationJsonPath $TranslationJsonPath `
    -OutputLocresPath $locresOutput

New-Item -ItemType Directory -Force $outputDir | Out-Null
New-Item -ItemType Directory -Force $stagingCultureDir | Out-Null

Copy-Item -LiteralPath $locresOutput -Destination (Join-Path $stagingCultureDir "$LocalizationTargetName.locres") -Force
New-GameLocmeta -Path $locmetaOutput -ExtraCulture $CultureCode
Copy-Item -LiteralPath $locmetaOutput -Destination (Join-Path $stagingGameLocDir "$LocalizationTargetName.locmeta") -Force

$responseLines = @(
    '"' + (Join-Path $stagingGameLocDir "$LocalizationTargetName.locmeta") + '" "../../../' + $GameName + '/Content/Localization/Game/' + $LocalizationTargetName + '.locmeta"'
    '"' + (Join-Path $stagingCultureDir "$LocalizationTargetName.locres") + '" "../../../' + $GameName + '/Content/Localization/Game/' + $CultureFolder + '/' + $LocalizationTargetName + '.locres"'
)
Set-Content -LiteralPath $responseFile -Value $responseLines -Encoding ASCII

foreach ($path in @($pakOutput, $utocOutput, $ucasOutput)) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Force
    }
}

& $UnrealPakPath $pakOutput "-create=$responseFile"
if ($LASTEXITCODE -ne 0) {
    throw "UnrealPak failed with exit code $LASTEXITCODE"
}

& $RetocPath to-zen --version UE5_6 $pakOutput $utocOutput
if ($LASTEXITCODE -ne 0) {
    throw "retoc failed with exit code $LASTEXITCODE"
}

if ($CreateZip) {
    $zipDir = Split-Path -Parent $zipOutput
    New-Item -ItemType Directory -Force $zipDir | Out-Null
    if (Test-Path -LiteralPath $zipOutput) {
        Remove-Item -LiteralPath $zipOutput -Force
    }

    Compress-Archive `
        -LiteralPath @($pakOutput, $utocOutput, $ucasOutput) `
        -DestinationPath $zipOutput `
        -CompressionLevel Optimal
}

if ($DeployToGame) {
    $cleanupNames = @(
        "pakchunk4242-Windows_P",
        "pakchunk9999-Windows_P",
        "pakchunk7777-BG-Windows_P",
        "Subnautica2-BG_P",
        $PackageName
    )

    foreach ($name in $cleanupNames) {
        foreach ($ext in @("pak", "ucas", "utoc")) {
            $target = Join-Path $GamePaksDir "$name.$ext"
            if (Test-Path -LiteralPath $target) {
                Remove-Item -LiteralPath $target -Force
            }
        }
    }

    Copy-Item -LiteralPath $pakOutput -Destination (Join-Path $GamePaksDir "$PackageName.pak") -Force
    Copy-Item -LiteralPath $utocOutput -Destination (Join-Path $GamePaksDir "$PackageName.utoc") -Force
    Copy-Item -LiteralPath $ucasOutput -Destination (Join-Path $GamePaksDir "$PackageName.ucas") -Force

    Write-Host "Standalone localization release built and deployed:"
    Write-Host " - " (Join-Path $GamePaksDir "$PackageName.pak")
    Write-Host " - " (Join-Path $GamePaksDir "$PackageName.utoc")
    Write-Host " - " (Join-Path $GamePaksDir "$PackageName.ucas")
    if ($CreateZip) {
        Write-Host " - " $zipOutput
    }
}
else {
    Write-Host "Standalone localization release built:"
    Write-Host " - " $pakOutput
    Write-Host " - " $utocOutput
    Write-Host " - " $ucasOutput
    Write-Host " - " $locmetaOutput
    if ($CreateZip) {
        Write-Host " - " $zipOutput
    }
}
