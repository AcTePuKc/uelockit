# Release Checklist

Use this checklist before publishing `UELocKit`.

## Repository content

- Remove project-specific extracted game files
- Remove project-specific translation working files
- Remove generated build outputs
- Keep only scripts, docs, config samples, and safe helper files

## Documentation

- README is clear and English-first
- Tool responsibilities are documented
- Workflow is documented
- IO Store packaging limits are documented
- Scope clearly says the toolkit works with existing keys, not arbitrary new ones

## Tooling

- Scripts work without hardcoded machine paths
- Scripts can use config and/or environment variables
- Build works without requiring bundled binaries in the repo

## Policy

- No proprietary game assets in the repo
- No original extracted `.locres` from a commercial game
- No local machine config committed

## Optional before first public release

- Pick a license
- Add upstream links for UnrealLocres, retoc, and any recommended inspection tool
- Add a simple example workspace layout image or diagram
- Add a minimal GitHub Pages docs setup
