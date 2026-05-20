---
layout: page
title: IO Store Packaging
permalink: /iostore-packaging/
---

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
