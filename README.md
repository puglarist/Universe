# Universe

Patch-driven game development workspace for **Universe**.

## Current Milestone
- **Patch 0 – Foundation Setup** (in progress): baseline repository, Unity setup plan, AI sandbox scaffolding, and build/test checklist.
- Detailed task definition: [`docs/roadmap/patch-000-foundation-setup.md`](docs/roadmap/patch-000-foundation-setup.md)

## Repository Structure
- `assets/` – Models, textures, animations, procedural assets, and placeholders.
- `scripts/` – Build automation, AI utility scripts, and development tooling.
- `ai/` – AI modules and prompt assets.
- `unity/` – Unity-specific setup notes and scene placeholders.
- `docs/` – Roadmaps, standards, task tracking, engine setup, and build guides.

## Quick Start
1. Read contribution and standards docs:
   - [`CONTRIBUTING.md`](CONTRIBUTING.md)
   - [`docs/standards/naming-versioning.md`](docs/standards/naming-versioning.md)
2. Execute Patch 0 checklist:
   - [`docs/roadmap/patch-000-foundation-setup.md`](docs/roadmap/patch-000-foundation-setup.md)
3. Validate AI sandbox wiring:
   - [`ai/modules/gpt_sandbox.py`](ai/modules/gpt_sandbox.py)

## Branching Convention
- `main` for stable integration.
- `patch-000-foundation-setup` for this milestone.
- Subsequent work should follow `patch-XYZ-topic` format, e.g.:
  - `patch-001-core-engine`
  - `patch-002-ai`
  - `patch-003-physics`

## Task Tracking
Use [`docs/task-tracking/roadmap-board-template.md`](docs/task-tracking/roadmap-board-template.md) to initialize GitHub Projects/Jira/Trello board columns and fields for 200+ tasks.
