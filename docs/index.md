---
layout: page
title: Home
permalink: /
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">Home</a>
  <a href="{{ '/quickstart/' | relative_url }}">Quickstart</a>
  <a href="{{ '/workflow/' | relative_url }}">Workflow</a>
  <a href="{{ '/tools/' | relative_url }}">Tools</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# UELocKit

`UELocKit` is a small toolkit for building Unreal Engine localization mods from existing in-game strings.

It is intended for translators and modders who want a repeatable workflow for:
- editing translations safely
- rebuilding `.locres`
- generating `.locmeta`
- packaging localization mods into `.pak`
- converting to `.utoc` and `.ucas` when the game uses IO Store

## Start here

- [Overview](./overview.md)
- [Quickstart](./quickstart.md)
- [Workflow](./workflow.md)
- [Tools](./tools.md)
- [IO Store Packaging](./iostore-packaging.md)
- [Release Checklist](./release-checklist.md)
- [Docs Localization Plan](./docs-localization-plan.md)

## Supported workflow

`UELocKit` supports a practical workflow built around:
- an existing source `.locres`
- an editable translation working file in `json` or `csv`
- generated working translation files created from the source `.locres`
- rebuilding translated localization outputs
- packaging those outputs for Unreal Engine games

## Non-goals

`UELocKit` does not try to:
- distribute original commercial game files
- distribute extracted proprietary localization files from games
- bundle third-party tools by default
- guarantee support for inventing brand-new localization keys in arbitrary Unreal games

## Important note

Users are expected to provide their own:
- extracted localization inputs
- local tool installations

This repo documents the workflow and provides scripts. It does not ship the extra files needed from a specific game installation.

<nav class="doc-nav">
  <a href="{{ '/quickstart/' | relative_url }}">Next: Quickstart</a>
</nav>
