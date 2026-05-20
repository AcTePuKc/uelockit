---
layout: page
title: IO Store Packaging
permalink: /iostore-packaging/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/quickstart/' | relative_url }}">Quickstart</a>
  <a href="{{ '/workflow/' | relative_url }}">Workflow</a>
  <a href="{{ '/tools/' | relative_url }}">Tools</a>
</nav>

# IO Store Packaging

Some Unreal Engine games expect localization content inside IO Store packaging rather than as loose files alone.

`UELocKit` supports that pattern by building:
- a translated `.locres`
- a generated `.locmeta`
- a `.pak`
- converted `.utoc` and `.ucas`

## Current flow

1. Build `Game.locres`
2. Generate `Game.locmeta`
3. Stage both files into the expected Unreal localization folder layout
4. Create a `.pak` with `UnrealPak.exe`
5. Convert the `.pak` to `.utoc` and `.ucas` with `retoc`
6. Optionally deploy the results to the game `Paks` directory

## Important limitation

Packaging rules are not universal across every Unreal title.

The pattern is reusable, but each game may differ in:
- naming conventions
- package priority
- mount paths
- required culture codes
- whether IO Store conversion is needed at all

<nav class="doc-nav">
  <a href="{{ '/tools/' | relative_url }}">Previous: Tools</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">Open Bulgarian version</a>
  <a href="{{ '/' | relative_url }}">Back to Home</a>
</nav>
