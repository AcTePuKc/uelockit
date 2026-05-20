# UELocKit

`UELocKit` is a small Unreal Engine localization modding toolkit for workflows based on existing game strings.

It is built around a few practical goals:
- edit translations in a safe working format
- rebuild translated `.locres` files
- generate `.locmeta`
- package localization mods for Unreal games that use `.pak` and optionally IO Store
- document the process without redistributing original game files or third-party binaries

## Scope

`UELocKit` is for translating existing localization keys that already exist in a game.

It is not a general framework for inventing brand-new localization keys and assuming every Unreal game will display them.

## License

- [MIT License](./LICENSE)

## Repository structure

- [build-locres.ps1](./build-locres.ps1)
- [tools/build-standalone-locmod.ps1](./tools/build-standalone-locmod.ps1)
- [tools/init_workspace.py](./tools/init_workspace.py)
- [tools/translation_io.py](./tools/translation_io.py)
- [tools/check_translation.py](./tools/check_translation.py)
- [config/UELocKit.sample.config.psd1](./config/UELocKit.sample.config.psd1)
- [docs/overview.md](./docs/overview.md)
- [docs/quickstart.md](./docs/quickstart.md)
- [docs/index.md](./docs/index.md)
- [docs/workflow.md](./docs/workflow.md)
- [docs/tools.md](./docs/tools.md)
- [docs/iostore-packaging.md](./docs/iostore-packaging.md)
- [docs/release-checklist.md](./docs/release-checklist.md)
- [docs/docs-localization-plan.md](./docs/docs-localization-plan.md)

## What users bring themselves

- Their own game-specific extracted localization files
- Their own local copies of external tools

## What this repo should not ship

- Original game archives
- Extracted proprietary game files
- Bundled third-party binaries unless there is a deliberate reason to vendor them

Users are expected to obtain those external inputs and tools themselves.

## Start here

1. Read [docs/tools.md](./docs/tools.md)
2. Read [docs/quickstart.md](./docs/quickstart.md)
3. Copy [config/UELocKit.sample.config.psd1](./config/UELocKit.sample.config.psd1) to `config/UELocKit.config.psd1`
4. Add your source `.locres`
5. Point the config at your files and tools
6. Initialize the working translation files
7. Edit the generated JSON working file
8. Build and test
