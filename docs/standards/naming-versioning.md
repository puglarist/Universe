# Naming, Standards, and Versioning

## Branch Naming
- `patch-XYZ-topic` where `XYZ` is zero-padded patch number.

## Folder Naming
- Use lowercase kebab-case for top-level non-code folders.
- Keep asset type grouping explicit (`models/`, `textures/`, etc.).

## Script/File Naming
- Python modules: `snake_case.py`
- Markdown docs: `kebab-case.md`

## Versioning
- Patch milestones: `0.x` while foundation is stabilizing.
- Move to `1.0.0` once baseline gameplay loop + build pipeline are production-ready.

## Coding Standards Baseline
- Keep modules single-purpose and testable.
- Prefer explicit configuration via environment variables.
- Avoid embedding secrets; use `.env` files excluded from VCS.
