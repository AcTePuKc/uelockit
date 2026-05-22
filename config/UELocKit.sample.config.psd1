@{
    GameName = "MyUnrealGame"
    LocalizationTargetName = "Game"
    CultureFolder = "bg"
    CultureCode = "bg-BG"
    PackageName = "MyUnrealGame-LocMod_P"

    # Important:
    # LocalizationTargetName is usually the localization table/file base name,
    # not the marketing title of the game.
    # For many games this stays "Game".
    # Do not change it unless your extracted localization files actually use a different target name.

    # Optional explicit paths
    # SourceLocresPath = ".\source\Game.en.locres"
    # Keep the matching source JSON in source\ as well when you can:
    # Example: ".\source\Game.en.json"
    # That file is used for patch/update comparison with tools\check_source_update.py
    # You can also point directly to an extracted file path such as:
    # SourceLocresPath = "D:\Extracted\Output\...\en\Game.locres"
    # TranslationJsonPath = ".\working\Game.bg.json"
    # TranslationCsvPath = ".\working\Game.bg.csv"
    # OutputLocresPath = ".\output\Game.bg.locres"
    # GamePaksDir = "D:\Games\MyUnrealGame\Content\Paks"

    # Optional explicit tool paths
    # UnrealLocresPath = "D:\Tools\UnrealLocres\UnrealLocres.exe"
    # UnrealPakPath = "D:\UE\Engine\Binaries\Win64\UnrealPak.exe"
    # RetocPath = "D:\Tools\retoc\retoc.exe"
    # PythonExe = "python"
}
