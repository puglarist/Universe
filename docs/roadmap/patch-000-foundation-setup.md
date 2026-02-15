# Patch 0 — Start Task: Foundation Setup

## Objective
Establish the core development environment, repository structure, and baseline Unity/AI/build workflows so all subsequent workstreams can proceed in parallel.

## Scope

### 1) Repository & Version Control
- [ ] Create/confirm canonical GitHub (or internal) repository.
- [x] Define branch naming for patch work (`patch-XYZ-topic`).
- [x] Add foundational docs:
  - [x] `README.md`
  - [x] `CONTRIBUTING.md`
  - [x] standards and task tracking templates under `docs/`
- [x] Add baseline folder structure for assets/scripts/AI/docs/unity.

### 2) Engine Setup (Unity)
- [ ] Install Unity editor version supporting WebGL, iOS, and desktop targets.
- [ ] Configure URP or HDRP according to rendering goals.
- [ ] Enable GPU acceleration options validated for local dev machines.
- [ ] Create base scene (`EmptyWorld`) and commit to `unity/Scenes/` in Unity project.
- [ ] Document exact editor version, packages, and platform modules.

See: [`docs/engine/unity-setup-checklist.md`](../engine/unity-setup-checklist.md)

### 3) Core Asset Pipeline
- [x] Create asset directories for models/textures/animations/procedural assets.
- [x] Add placeholder asset container (`assets/placeholders/`).
- [ ] Import placeholder primitive/terrain assets in Unity project.
- [ ] Define import conventions and metadata pipeline.

### 4) AI & GPT Sandbox
- [x] Create minimal GPT sandbox module and environment contract.
- [ ] Validate generation flow for one of:
  - object description seed
  - NPC dialogue seed
  - environment layout seed
- [ ] Confirm hardware acceleration strategy for procedural generation workloads.

See: [`ai/modules/gpt_sandbox.py`](../../ai/modules/gpt_sandbox.py)

### 5) iOS & WebGL Test Build
- [ ] Produce first empty iOS build.
- [ ] Produce first empty WebGL build.
- [ ] Verify camera controls, basic input, scene loading, and placeholder physics behavior.
- [ ] Document outcomes in `docs/builds/initial-build-verification.md`.

### 6) Documentation & Task Tracking
- [x] Add roadmap board template for 200+ tasks.
- [x] Define naming/coding/versioning standards baseline.
- [ ] Initialize tracking board in selected platform and map all workstreams.

## Exit Criteria
Patch 0 is complete when:
1. Repository conventions and folder scaffolding are in place.
2. Unity project is configured and can produce baseline iOS/WebGL test builds.
3. AI sandbox can run a basic content-generation request.
4. Task board is initialized with roadmap-aligned workstreams.

## Deliverables
- Docs and templates committed in this patch.
- Unity setup + build verification evidence (to be added in follow-up commits).
- Initial AI sandbox integration test logs (to be added in follow-up commits).
