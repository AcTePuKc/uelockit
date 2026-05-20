---
layout: page
title: Tools
permalink: /tools/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">BG</a>
  <a href="{{ '/quickstart/' | relative_url }}">Quickstart</a>
  <a href="{{ '/workflow/' | relative_url }}">Workflow</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# Tools

`UELocKit` uses a bring-your-own-tools model.

The toolkit provides scripts and documentation. The user provides local copies of the external tools.

For a normal user, the simplest mental model should be:
- place the required source file in the expected folder
- make the external tools discoverable
- run the init script
- translate
- run the build scripts

## Upstream links

- `FModel`
  GitHub: [4sval/FModel](https://github.com/4sval/FModel)
  Releases: [FModel Releases](https://github.com/4sval/FModel/releases)
- `retoc`
  GitHub: [trumank/retoc](https://github.com/trumank/retoc/)
- `UnrealPak`
  Comes with Unreal Engine.
  Reference overview: [UnrealPak overview](https://unrealpak.com/)

## What to use, and when

### FModel

Use FModel when you want to:
- inspect game assets visually
- browse localization-related assets
- export contextual JSON or text views when available

FModel is mainly useful for discovery and context, not for rebuilding `.locres`.

### retoc

Use `retoc` when you want to:
- inspect or work with IO Store-based Unreal game content
- convert packaging outputs when the game expects `.utoc` and `.ucas`

In this toolkit, `retoc` is part of the packaging stage.

### UnrealLocres

Use `UnrealLocres` when you want to:
- export or import `.locres`
- rebuild a translated `.locres` from CSV

This is the key tool for the actual localization data round-trip.

### UnrealPak

Use `UnrealPak.exe` when you want to:
- create the `.pak` that will contain the translated localization files

### Python

Use Python when you want to:
- initialize a translation workspace from a source `.locres`
- convert JSON to CSV
- convert CSV to JSON
- validate translation working files
- run lightweight helper scripts

### PowerShell

Use PowerShell when you want to:
- orchestrate the full build
- stage files into the right Unreal folder structure
- generate `.locmeta`
- call the external tools in sequence

### Python build entrypoint

Use the Python build entrypoint when you want:
- a less Windows-specific orchestration layer
- a script that is easier to adapt for CI or automation
- a build flow that is not tied only to PowerShell

Current script:
- [build_locmod.py](../tools/build_locmod.py)

## Tool discovery

The scripts look for tools in this order:

1. Explicit parameter
2. Environment variable
3. Local workspace convention

## Environment variables

- `UNREALLOCRES_EXE`
- `UNREALPAK_EXE`
- `RETOC_EXE`

## Config file

Sample config:
- [UELocKit.sample.config.psd1](../config/UELocKit.sample.config.psd1)

Recommended local pattern:
- copy it to `config/UELocKit.config.psd1`
- keep the real config file out of version control

## Recommended public-repo policy

- document upstream tools
- link to upstream projects
- do not bundle the binaries unless you explicitly choose to vendor them later

## What the toolkit does for the user

If the user provides:
- a source `.locres`
- local tool installations
- a valid config or command-line paths

then the toolkit can:
- generate the initial working translation files
- rebuild a translated `.locres`
- generate `.locmeta`
- build `.pak`
- convert or package `.utoc` and `.ucas`

Preferred translation editing target:
- the generated JSON working file

Compatibility target:
- the generated CSV working file

What it does not provide:
- the original extracted game files
- the external binaries
- game-specific reverse engineering beyond this workflow

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Read this page in Bulgarian</a>
  <a href="{{ '/workflow/' | relative_url }}">Previous: Workflow</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Next: Packaging</a>
</nav>
