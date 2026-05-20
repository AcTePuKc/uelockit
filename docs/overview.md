# Overview

`UELocKit` is a practical workflow for translating existing Unreal Engine localization strings and shipping them as a localization mod.

## Core idea

- extract or obtain an existing `.locres`
- convert it into a safe editable working format
- translate existing strings
- rebuild a translated `.locres`
- package the result for the target game

## Intended audience

- translators
- modders
- technical localizers
- players who want to build a translation for a game that does not officially support their language

## Supported workflow

The toolkit is meant for projects where you can:
- obtain an existing source `.locres`
- inspect the game’s localization context with external tools
- translate existing keys
- rebuild and package the result

## Important boundary

`UELocKit` is about working with existing localization keys that a game already uses.

It does not assume that you can:
- invent a brand-new localization key
- inject it into every Unreal game
- have the game automatically display it

That is game-specific behavior and should not be promised by a generic toolkit.

## Additional non-goal

`UELocKit` does not distribute the extra files needed from a specific game installation.

Users must provide:
- their own extracted localization inputs
- their own local copies of third-party tools
