# Workflow

## High-level flow

1. Obtain the source localization files from a game you are allowed to inspect for modding or personal translation use.
2. Inspect or export the localization with your chosen tools.
3. Copy the extracted source files into `source/`.
4. Initialize the workspace from the source `.locres`.
5. Keep the extracted `Game.json` in `source/` for future patch comparisons.
6. Translate the `target` text while preserving keys and placeholders.
7. Rebuild a translated `.locres`.
8. Generate `.locmeta`.
9. Package the result into `.pak`.
10. Convert or package to `.utoc` and `.ucas` if the target game uses IO Store.
11. Test in-game.
12. Repeat for playtest fixes and terminology cleanup.

## Suggested working files

- `working/<target>.<culture>.json`
- `working/<target>.<culture>.csv`
- `working/<target>.en.csv`

Example:
- `working/Game.bg.json`
- `working/Game.bg.csv`
- `working/Game.en.csv`

Common extracted source example:
- `Output/.../en/Game.locres`
- `Output/.../en/Game.json`

Common local working convention inside `UELocKit`:
- `source/Game.en.locres`
- `source/Game.en.json`

Preferred editing file:
- edit `working/<target>.<culture>.json`

Compatibility file:
- `working/<target>.<culture>.csv` exists for import/export compatibility, not because it is the preferred editing format

## Choosing the output culture

The user chooses the culture through two values:

- `CultureTag`
  Used in working file names and usually in the localization folder name
- `CultureCode`
  Used when generating `.locmeta`

Examples:
- `bg` and `bg-BG`
- `pl` and `pl-PL`
- `th` and `th-TH`

In the current toolkit, the easiest place to set them is:
- `config/UELocKit.config.psd1`

Important:
- `LocalizationTargetName` is usually the localization file base name, not the title of the game
- for many games it stays `Game`
- changing it incorrectly will make the scripts look for the wrong files

## Editing rules

- Do not change localization keys unless you know exactly why.
- Do not change source text unless you are intentionally repairing your own working copy.
- Preserve placeholders such as `[InventoryActionPrimary]`.
- Preserve meaningful line breaks.
- Prefer JSON for multiline text and heavy narrative entries.

## Conversion commands

JSON to CSV:

```powershell
python .\tools\translation_io.py json-to-csv `
  --input .\working\Game.bg.json `
  --output .\working\Game.bg.csv
```

CSV to JSON:

```powershell
python .\tools\translation_io.py csv-to-json `
  --input .\working\Game.bg.csv `
  --output .\working\Game.bg.json
```

## Workspace initialization

If the user starts only with a source `.locres`, `UELocKit` can generate the initial working files.

Example:

```powershell
python .\tools\init_workspace.py `
  --workspace-root . `
  --source-locres .\source\Game.en.locres `
  --localization-target Game `
  --culture-tag bg
```

This generates:
- `working/Game.en.csv`
- `working/Game.bg.csv`
- `working/Game.bg.json`

That is the missing bootstrap step before normal translation work starts.

## Continuing from an existing translation

If the user already has a translation, the goal is different:
- do not start from an empty `target`
- instead, convert or refresh the existing translation into the row-based working format
- continue editing there

This is the correct path for:
- an existing translated `Game.json`
- an existing translated `.locres`
- a game-specific helper that imports another translation format into the standard working JSON

In other words:
- `init_workspace` is for a new translation
- a refresh or import step is for an existing translation

## Patch update checks

When the game updates, extract the new source `Game.json` again and copy it into `source/`.

Then compare it against your current working translation file:

```powershell
python .\tools\check_source_update.py `
  --working .\working\Game.bg.json `
  --source-json .\source\Game.en.json
```

That gives you a quick report for:
- added keys
- removed keys
- changed source values

This is the safest way to tell whether a new patch actually changed the localizable strings before you rebuild or continue translating.

## Build commands

Build `.locres`:

```powershell
& .\build-locres.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

Build standalone package:

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

Build without automatic deployment:

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json `
  -DeployToGame $false
```
