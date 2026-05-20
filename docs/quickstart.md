---
layout: page
title: Quickstart
permalink: /quickstart/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">BG</a>
  <a href="{{ '/workflow/' | relative_url }}">Workflow</a>
  <a href="{{ '/tools/' | relative_url }}">Tools</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# Quickstart

This is the shortest path from a source `.locres` file to a buildable translation workspace.

## 1. Extract or obtain the source localization

Use your preferred inspection or extraction tool to obtain the source localization file from the game.

Most commonly, you want something like:
- `Game.locres`

If you extract with a tool such as FModel, you may end up with a path like:
- `Output/.../en/Game.locres`

That is normal.

The source language does not have to be English if your workflow is based on another existing language.

For example, your extracted source might come from:
- `Output/.../en/Game.locres`
- `Output/.../fr/Game.locres`
- `Output/.../de/Game.locres`

You do not need the extracted file itself to already be named `Game.en.locres`.

For a default Unreal-style setup in this toolkit, the easiest convention is:
- copy or point that extracted file to a clear local working path such as:
  - `source/Game.en.locres`
  - `source/Game.fr.locres`
  - `source/Game.de.locres`

If your project uses a different localization target name, you can reflect that in the config.

## 2. Put your files in place

Place these in your local `UELocKit` workspace:

- your source localization file somewhere accessible
  Example extracted path: `Output/.../en/Game.locres`
- optionally copy it into `source/`
  Example local working path: `source/Game.en.locres`
- the required external tools somewhere on your machine

You do not need to copy every tool into the repo folder if you prefer environment variables or explicit paths.

## 3. Choose your language

There are two values to think about:

- `CultureTag`
  Short folder/file tag used by the workspace
  Example: `bg`, `pl`, `th`
- `CultureCode`
  Full Unreal culture code used in `locmeta`
  Example: `bg-BG`, `pl-PL`, `th-TH`

You set those in:
- `config/UELocKit.config.psd1`

Start by copying:
- `config/UELocKit.sample.config.psd1`

to:
- `config/UELocKit.config.psd1`

Then edit:
- `CultureFolder`
- `CultureCode`
- `LocalizationTargetName`
- `GameName`
- tool paths if needed

Important:
- `LocalizationTargetName` is usually the localization table/file base name, not the name of the game
- for many games it should stay `Game`
- do not change it unless your extracted localization files clearly use a different target name

## 4. Make the tools discoverable

You have three choices:

1. Put the tools in the expected local locations
2. Set environment variables
3. Pass explicit paths to the scripts

Environment variables supported:
- `UNREALLOCRES_EXE`
- `UNREALPAK_EXE`
- `RETOC_EXE`

## 5. Initialize the workspace

If you want the simplest command for Windows users:

```powershell
& .\tools\init_workspace.ps1
```

That simple command assumes your local working copy of the source file follows the default convention:
- `source/Game.en.locres`

If you prefer Python directly:

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

The generated names depend on your target name and culture tag.

## 6. Translate

Edit the generated JSON working file.

That is the main file translators should work in.

The generated CSV file exists for compatibility and import/export workflows, but the preferred editing file is the JSON file.

Example:
- `working/Game.bg.json`

## 7. Build translated locres

```powershell
& .\build-locres.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

## 8. Build the mod package

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

This generates:
- translated `.locres`
- `.locmeta`
- `.pak`
- `.utoc`
- `.ucas`

## 9. About the output package name

The output package name is configurable.

In most cases, the exact filename is not the important part. What matters more is:
- that it is unique
- that it does not collide with another mod package
- that it follows whatever naming convention works best for the target game or community

Depending on the target game, common naming patterns might look like:
- `MyGame-LocMod_P`
- `MyGame-BG_P`
- `pakchunk9999-Localization-Windows_P`

The toolkit uses a default such as:
- `MyUnrealGame-LocMod_P`

You can change that in:
- `config/UELocKit.config.psd1`

If a specific game turns out to care about load order, chunk naming, or platform suffix conventions, document that game-specific rule separately and follow it there.

## Important note

`UELocKit` does not provide:
- your game files
- your extracted source localization
- bundled third-party tools

You must supply those yourself.

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Read this page in Bulgarian</a>
  <a href="{{ '/' | relative_url }}">Previous: Home</a>
  <a href="{{ '/workflow/' | relative_url }}">Next: Workflow</a>
</nav>
