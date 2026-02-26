# Codex + Universe v1.0 Genesis Stable — Master Start Task + Core Updates

## A) CODEX PLATFORM UPDATE MAP (NEW WORK NEEDED)

### A1) Codex Boot + Mode Switcher
- Add canonical boot handshake: `Codex is now open.` plus current world and patchline context.
- Enforce Universe-only context lock (reject cross-domain modules by default).
- Implement runtime modes:
  - **Builder**: edit schema/API/patch definitions.
  - **Operator**: run builds, tests, export bundles.
  - **Observer**: read-only dashboards and logs.

### A2) Identity Gate (Face ID-ready design)
- Define auth flow with pluggable device-auth hook (Face ID placeholder interface).
- Session tokens: short-lived access token + renewable session token; idle and absolute timeout.
- Re-auth triggers: privilege escalation, export, permission changes, stale session.
- Permission tiers: **Owner / Builder / Tester / Viewer** with explicit capability matrix.

### A3) Worlds Menu
- Build world registry metadata model: `world_id`, name, semantic version, tags, last build hash/time.
- Actions: **Create / Fork / Archive / Export** with audit entries.
- Add “Universe Reset & Fork” guardrails: dry-run diff, destructive-action warning, snapshot-before-reset.

### A4) Patchline Manager (Core)
- Patch registry fields: patch number, status, owner, dependencies, artifact pointers.
- Auto-generate changelog/release-note skeleton from merged tasks.
- Add `Start Patch` command that creates folder template, checklist, and default test plan.

### A5) Debug Console + Telemetry
- Define commands: `validate_schema`, `run_tests`, `profile_webgl`, `export_build`, `diff_worlds`.
- Logging levels: TRACE/DEBUG/INFO/WARN/ERROR/FATAL; standardized run/session correlation IDs.
- Crash bundle format: logs + stack + environment + patch manifest.
- Telemetry: local-first ring-buffer metrics; opt-in remote sync flag reserved.

### A6) Artifact System
- Per-patch required directories: `docs/ schema/ api/ tests/ assets/ build/`.
- Export naming: `universe-patch-<##>-<semver>-<yyyymmdd>.zip`.
- Include checksum manifest and version tags in build metadata.

### A7) Compliance / Safety Guardrails
- Enforce simulation-only labeling in UI and release notes.
- Disallowed-output policy filter for real-world harm instructions.
- Immutable audit log for sensitive operations (exports, permission changes, archival/reset).

### A8) Performance & Budget Profile
- Define low-budget target profile for ~$900 workstation hardware.
- Establish WebGL baseline constraints and asset-streaming budget policy.
- Publish WebXR gateway path (feature-gated, progressive enhancement).

---

## B) START TASK: GENERATE THE FULL BACKLOG (AUTO)

| ID | Title | Description | Dependencies | Outputs (files/artifacts) | Acceptance Criteria | Tests |
|---|---|---|---|---|---|---|
| CODEx-001 | Boot Handshake + Context Lock | Implement `/codex boot` response, mode selection, universe scope validator. | None | `docs/boot-spec.md`, `api/boot.schema.json` | Boot returns canonical message and rejects non-Universe context in all modes. | Unit test for boot payload; integration test for scope rejection. |
| CODEx-002 | Runtime Mode Permissions | Define Builder/Operator/Observer capabilities and mode switch behavior. | CODEx-001 | `docs/modes-matrix.md` | Unauthorized actions blocked per mode matrix. | Permission matrix tests across commands. |
| CODEx-003 | Identity Gate Core | Add auth flow, token lifecycle, re-auth triggers. | CODEx-002 | `docs/auth-flow.md`, `api/auth.openapi.yaml` | Session expires correctly; re-auth required on sensitive actions. | Session timeout tests + escalation-path tests. |
| CODEx-004 | Device Auth Hook Interface | Add Face ID-ready adapter contract (placeholder provider). | CODEx-003 | `api/device-auth.interface.md` | Device hook can be swapped without API changes. | Contract tests with mock provider. |
| CODEx-005 | Permission Tier System | Implement Owner/Builder/Tester/Viewer role map with explicit capabilities. | CODEx-003 | `docs/permissions.md` | Role checks gate all sensitive operations and emit audit entries. | RBAC integration test suite. |
| CODEx-006 | Worlds Registry | Create world registry model and persistence ops. | CODEx-001 | `schema/world-registry.sql`, `api/worlds.openapi.yaml` | Worlds list/create/fork/archive/export metadata persists and validates. | CRUD tests + schema migration test. |
| CODEx-007 | Reset & Fork Safety | Add snapshot, diff preview, confirmation flow. | CODEx-006 | `docs/reset-fork-guardrails.md` | Reset blocked unless snapshot + explicit confirmation completed. | Destructive-action guard tests. |
| CODEx-008 | Patch Registry Core | Define patch entity lifecycle and dependency tracking. | CODEx-001 | `schema/patch-registry.sql`, `docs/patch-state-model.md` | Patch status transitions valid and dependency cycles rejected. | State machine + cycle detection tests. |
| CODEx-009 | Start Patch Automation | Build `/patch start <#>` scaffold generator and checklist initializer. | CODEx-008, CODEx-006 | `scripts/start_patch.sh`, generated patch folders | Command creates complete template with IDs/checks/tests sections. | Golden-file scaffold test. |
| CODEx-010 | Changelog + Notes Generator | Auto-generate changelog and release-note drafts from task metadata. | CODEx-008 | `scripts/generate_release_notes.sh`, `docs/templates/*.md` | Generated docs include all closed tasks and artifact checksums. | Snapshot tests on generated markdown. |
| CODEx-011 | Debug Command Surface | Implement validate/run/profile/export/diff command handlers. | CODEx-001, CODEx-008 | `api/debug.openapi.yaml`, `docs/debug-commands.md` | All debug commands return structured result payloads. | CLI contract tests per command. |
| CODEx-012 | Telemetry + Crash Bundles | Add local telemetry buffer and crash bundle schema. | CODEx-011 | `schema/crash-bundle.json`, `docs/telemetry-plan.md` | Crash bundle is reproducible and includes mandatory fields. | Simulated crash test + bundle validator. |
| CODEx-013 | Artifact Packaging Standard | Enforce folder structure, export naming, checksum manifest. | CODEx-009 | `docs/artifact-standard.md`, `scripts/package_patch.sh` | Export zip always contains required directories and manifest. | Packaging integration test. |
| CODEx-014 | Compliance Guardrails | Add simulation labeling, harmful-output filter, audit log policy. | CODEx-003, CODEx-005 | `docs/compliance-policy.md`, `schema/audit-log.sql` | Sensitive actions are logged and unsafe output paths are blocked. | Policy tests + audit insert tests. |
| CODEx-015 | Performance Budget Profiles | Define workstation baseline, WebGL budgets, XR gateway switches. | CODEx-011 | `docs/perf-budget.md`, `docs/xr-gateway.md` | Build profile validates against CPU/GPU/RAM/asset budgets. | Performance budget linter test. |

---

## C) UNIVERSE BACKLOG (RE-CONSTITUTE FROM PATCH 1–67)

### C1) Freeze Baseline: “Universe v1.0 Genesis Stable”

**Included Features (baseline IN):**
1. Core universe simulation loop with configurable tick rate.
2. Multi-world concept with world-level identity.
3. Initial realism framework and simulation constraints.
4. Combat simulation mechanics (simulation-safe abstraction only).
5. Justice chain initiation from incident to court entry.
6. Economy model foundations (agents, markets, resource flows).
7. Civil authority presence (cops/military simulation entities).
8. Early court process scaffolding and legal-state transitions.
9. Event-driven world state mutation model.
10. Build artifact generation for patch-level exports.
11. Incremental patch history through Patch 67.
12. Foundational debugging hooks and log capture.
13. Initial content modules for scenario variation.
14. Entity tagging/classification for behavior routing.
15. Basic balancing knobs for population/economy parameters.
16. Save-state prototypes (non-standardized).
17. Replay/debug traces in partial form.
18. Initial menu/shell entry points for operations.
19. Version-tagged conceptual expansion planning (“50x expansion”).
20. Early performance tuning attempts without unified budget targets.

**Baseline OUT (not in v1.0 freeze):**
- Production-grade identity gate and session governance.
- Fully formalized persistence schema and migrations.
- Stable public API contract and event bus spec.
- Deterministic replay guarantee for QA sign-off.
- WebXR shipping profile and validated device matrix.
- Automated release manager with signed checksum bundles.

### C2) Gap Map (UNSTARTED FORMALIZATION)
- Architecture diagram (text-based) with module boundaries and runtime ownership.
- Persistence schema covering entities, relations, and migration policy.
- API surface spec: management REST + simulation event contracts.
- AI scaling design for population behavior and economy feedback loops.
- Performance plan for WebGL/XR plus offline-lite operation.
- Phase I–VII rollout sequence with entry/exit gates.
- Test harness with deterministic replay and regression snapshots.
- Codex security gate integration (authN/authZ/audit).

---

## D) PATCH SERIES (CREATE MORE UPDATES — CODEX + UNIVERSE)

### D0) Patch 68 — CONSOLIDATION + DEBUG RELEASE (Universe)
**Goals**
- Freeze v1.0 baseline, normalize module map, and deliver debug-ready release candidate.

**Task List**
- P68-T01 Baseline inventory lock (artifact: `docs/p68-baseline-lock.md`).
- P68-T02 Module dependency map (artifact: `docs/p68-architecture-map.md`).
- P68-T03 Debug command smoke suite (artifact: `tests/p68-debug-smoke.md`).
- P68-T04 Release candidate bundle + checksum (artifact: `build/p68-rc.zip`, manifest).

**Acceptance Criteria**
- Baseline IN/OUT approved and immutable for subsequent patches.
- All debug commands execute against baseline with structured output.

**Test Plan**
- Smoke run of five debug commands.
- Verify checksum manifest reproducibility.

**Risks + Mitigations**
- Risk: hidden scope creep in baseline freeze.
- Mitigation: strict change-control label and deferred queue.

**Done Means**
- Baseline frozen, RC artifact exported, and patch status marked `closed-debug-ready`.

### D1) Patch 69 — Persistence Schema + Save/Load + Versioned Worlds
**Goals**
- Formalize persistence model and deterministic save/load lifecycle.

**Task List**
- P69-T01 Entity-relationship schema v1.
- P69-T02 Migration pipeline + rollback tags.
- P69-T03 Save/load API and version conversion adapters.
- P69-T04 World version metadata enforcement.

**Acceptance Criteria**
- Save/load round-trip fidelity ≥ 99.9% for canonical scenarios.
- Schema migrations are reversible in staging.

**Test Plan**
- Migration forward/backward tests.
- Save/load deterministic replay comparison.

**Risks + Mitigations**
- Risk: schema drift across worlds.
- Mitigation: version pinning + converter registry.

**Done Means**
- Schema, migrations, and world versioning are documented, tested, and shipped.

### D2) Patch 70 — AI Population + Behavior Grid + Economy Balancing
**Goals**
- Scale agents with deterministic behavior grid and stable economy balancing.

**Task List**
- P70-T01 Behavior grid model (roles, states, transitions).
- P70-T02 Population scaling controller.
- P70-T03 Economy balancing pass with guardrails.
- P70-T04 AI metrics dashboard for anomaly detection.

**Acceptance Criteria**
- Population simulation scales to target profile without instability spikes.
- Economy variance remains within defined tolerances.

**Test Plan**
- Seeded long-run simulations (24h accelerated).
- Outlier detection assertions on market collapse metrics.

**Risks + Mitigations**
- Risk: emergent runaway feedback loops.
- Mitigation: rate limiters + circuit-breaker policies.

**Done Means**
- Stable, measurable AI/economy behavior under seeded workloads.

### D3) Patch 71 — Justice Loop Completion (simulation-safe)
**Goals**
- Complete courts → jail → prison → re-entry loop with compliance-safe abstractions.

**Task List**
- P71-T01 Legal-state machine completion.
- P71-T02 Sentencing/jail/prison simulation modules.
- P71-T03 Re-entry mechanics and recidivism balancing.
- P71-T04 Safety labeling + harmful-output filter validation.

**Acceptance Criteria**
- End-to-end justice loop executes with no undefined state transitions.
- Simulation-only labeling is present on all justice interfaces.

**Test Plan**
- Scenario tests from incident to re-entry across policy variants.
- Safety filter regression suite.

**Risks + Mitigations**
- Risk: policy bias in outcomes.
- Mitigation: configurable policy parameters + fairness telemetry.

**Done Means**
- Full justice pipeline modeled, tested, and compliance-labeled.

### D4) Patch 72 — WebGL/XR Performance + Asset Streaming + Offline-lite
**Goals**
- Hit WebGL performance targets, introduce streaming bundles, and offline-lite queues.

**Task List**
- P72-T01 WebGL budget instrumentation.
- P72-T02 Asset streaming bundle conversion.
- P72-T03 Offline-lite world slice cache + deferred sync queue.
- P72-T04 XR gateway toggles and fallback paths.

**Acceptance Criteria**
- Meets FPS/memory thresholds on target $900 profile.
- Offline-lite mode supports disconnected progression and safe resync.

**Test Plan**
- Performance benchmark suite on constrained profile.
- Offline/online reconciliation tests.

**Risks + Mitigations**
- Risk: memory fragmentation on large worlds.
- Mitigation: chunked loading + aggressive asset eviction.

**Done Means**
- Performance profile passes and offline-lite is validated.

### D5) Patch 73 — Codex Identity Gate + Permissions + Session Control
**Goals**
- Productionize authN/authZ/session controls for Codex operations.

**Task List**
- P73-T01 Auth flow implementation.
- P73-T02 Role-based access enforcement.
- P73-T03 Session timeout + re-auth triggers.
- P73-T04 Audit logging for sensitive operations.

**Acceptance Criteria**
- Unauthorized sensitive operations blocked 100% in automated tests.
- Audit trail complete for all permission and export events.

**Test Plan**
- RBAC matrix tests.
- Session expiry and re-auth integration tests.

**Risks + Mitigations**
- Risk: privilege escalation edge cases.
- Mitigation: deny-by-default policy + escalation tests.

**Done Means**
- Identity gate blocks/permits correctly with complete auditability.

### D6) Patch 74 — Worlds Menu + Fork/Reset + Diff Tooling
**Goals**
- Deliver robust world operations UI/CLI with safe reset/fork and diff visibility.

**Task List**
- P74-T01 World registry CRUD implementation.
- P74-T02 Fork/reset guarded workflows.
- P74-T03 World diff engine and summary report.
- P74-T04 Export action with manifest linkage.

**Acceptance Criteria**
- All world lifecycle actions produce valid registry/audit entries.
- Reset cannot proceed without snapshot + explicit confirmation.

**Test Plan**
- Lifecycle integration tests across create/fork/archive/export.
- Diff accuracy checks on controlled world mutations.

**Risks + Mitigations**
- Risk: accidental destructive operations.
- Mitigation: two-step confirmation + preflight snapshots.

**Done Means**
- Worlds menu is operational with safe, auditable lifecycle tooling.

### D7) Patch 75 — Patchline Manager + Release Automation + Export Bundles
**Goals**
- Automate patch lifecycle, release-note generation, and reproducible export bundles.

**Task List**
- P75-T01 Patch state machine + dependency resolver.
- P75-T02 Start/status/close command handlers.
- P75-T03 Changelog/release notes auto-generator.
- P75-T04 Bundle export + checksum + tag stamping.

**Acceptance Criteria**
- Patch workflow enforces dependencies and required checklists.
- Release bundle reproducible with stable checksums.

**Test Plan**
- End-to-end patch lifecycle tests.
- Reproducible build verification across two clean runs.

**Risks + Mitigations**
- Risk: artifact mismatch between notes and bundle.
- Mitigation: manifest lock + generation from single source of truth.

**Done Means**
- Patchline manager drives release automation with verified artifacts.

---

## E) DEBUG / QA SWEEP (MANDATORY; ASSIGN EVERY ISSUE)

| Issue | Severity | Fix Recommendation | Patch | Verification |
|---|---|---|---|---|
| E1-1 Contradiction: conceptual features > formal schema | P1 | Freeze baseline scope and map every feature to schema owner. | 68/69 | Baseline map has 100% feature-to-entity references. |
| E1-2 Contradiction: partial justice loop definitions | P1 | Complete legal-state machine with explicit transitions. | 71 | No undefined transition in state-machine tests. |
| E2-1 Missing dependency: patch registry before automation | P0 | Implement patch registry/state model first. | 75 | `/patch start/status/close` pass integration tests. |
| E2-2 Missing dependency: world versioning before diff/export | P1 | Add world semantic version model and converters. | 69/74 | Diff/export include version metadata and conversion logs. |
| E3-1 CPU bottleneck in large agent ticks | P1 | Batch updates + fixed timestep budget enforcement. | 70/72 | Tick budget alarms below threshold in profiling. |
| E3-2 GPU bottleneck from unbounded draw calls | P1 | Introduce LOD, batching, and streaming bundles. | 72 | Draw calls and frame time meet target envelope. |
| E3-3 RAM pressure from world state growth | P1 | Chunked world slices + eviction strategy. | 72 | Memory plateau sustained under stress test. |
| E4-1 WebGL memory ceiling risk | P0 | Cap texture/buffer budgets and preload windows. | 72 | Browser memory usage remains below configured cap. |
| E4-2 WebGL threading limitations | P2 | Move non-critical processing to deferred queues. | 72 | Main-thread frame spikes reduced in trace. |
| E4-3 I/O stalls on asset fetch | P2 | Predictive prefetch and cache hints. | 72 | Asset load stutter metrics improve by target %. |
| E5-1 Security gap: missing re-auth on export | P0 | Mandatory step-up auth for export operations. | 73 | Export blocked without re-auth in tests. |
| E5-2 Security gap: weak audit coverage | P1 | Immutable audit schema with sensitive action taxonomy. | 73 | 100% sensitive actions produce audit rows. |
| E5-3 Secret handling undefined for optional server mode | P1 | Introduce secret vault interface and rotation policy. | 73 | Secret retrieval + rotation test passes. |
| E6-1 Data model: missing migration contract | P0 | Define migration policy and semantic versions. | 69 | Forward/backward migration suite passes. |
| E6-2 Data model: inconsistent entity IDs | P1 | Standardize UUID format and namespace strategy. | 69 | ID validation check has zero violations. |
| E7-1 Release risk: version drift docs vs artifacts | P1 | Derive docs from manifest source-of-truth. | 75 | Version parity check passes in CI. |
| E7-2 Release risk: checksum not enforced | P0 | Require checksum file for close/release gates. | 75 | Release blocked when checksum missing/mismatch. |
| E8-1 Coverage gap: deterministic replay | P0 | Add seed-based replay harness with snapshots. | 69/70 | Replay outputs match baseline snapshots exactly. |
| E8-2 Coverage gap: destructive world ops | P1 | Expand reset/fork scenario suite with rollback checks. | 74 | No data loss in controlled destructive-op tests. |
| E8-3 Coverage gap: auth boundary regressions | P1 | Add cross-role command fuzz testing. | 73 | Unauthorized-path pass rate is 100%. |

---

## F) IMPLEMENTATION DEFAULTS (MAKE DECISIONS NOW)
- **Engine:** Unity WebGL baseline for web play; WebXR gateway for XR; native bridge deferred.
- **Data:** Local SQLite for world saves; optional Postgres path for server/multiplayer.
- **API:** REST for management; event bus for simulation ticks and domain events.
- **Assets:** glTF asset format with addressable streaming bundles.
- **Determinism:** Seed-based replay + fixed timestep simulation.
- **Offline-lite:** Cached world slices and deferred sync queue with conflict policy.

---

## G) STANDARD TEMPLATES (OUTPUT READY-TO-USE)

### G1) Folder Structure Template (per patch)
```text
patch-<##>/
  docs/
    overview.md
    architecture.md
    risks.md
  schema/
    migrations/
    models/
  api/
    openapi.yaml
    events.md
  tests/
    unit/
    integration/
    replay/
  assets/
    source/
    bundles/
  build/
    manifests/
    exports/
```

### G2) Changelog Template
```markdown
# Patch <##> Changelog
## Added
- 
## Changed
- 
## Fixed
- 
## Removed
- 
## Artifacts
- Bundle:
- Checksum:
- Manifest:
```

### G3) Release Notes Template
```markdown
# Universe Release Notes — Patch <##>
## Summary
## Key Features
## Breaking / Migration Notes
## Performance Impact
## Security & Compliance
## Known Issues
## Verification Matrix
## Download / Checksum
```

### G4) Test Plan Template
```markdown
# Patch <##> Test Plan
## Scope
## Entry Criteria
## Test Suites
- Unit
- Integration
- Replay/Determinism
- Performance
- Security
## Exit Criteria
## Defects Found
## Sign-off
```

### G5) “Start Patch” Checklist Template
```markdown
# Start Patch <##> Checklist
## Preflight
- [ ] Dependencies closed
- [ ] Scope frozen
- [ ] Risk register created
## Build
- [ ] Schema/API artifacts created
- [ ] Tests scaffolded
- [ ] Telemetry hooks added
## Verify
- [ ] Unit/integration/replay pass
- [ ] Performance budget check pass
- [ ] Security audit checks pass
## Export
- [ ] Changelog generated
- [ ] Release notes generated
- [ ] Bundle + checksum generated
- [ ] Patch status moved to ready/closed
```

---

## H) EXECUTION COMMANDS (CODEX OPERATIONS)

- `/codex boot`
  - **Output:** boot message, active mode, universe lock status, active patchline summary.

- `/worlds list`
  - **Output:** table of worlds (`world_id`, name, version, tags, last build, status).

- `/worlds create <name> [--from-template <id>]`
  - **Output:** new world record, initial version, artifact scaffold path.

- `/worlds fork <world_id> --as <new_name>`
  - **Output:** fork result with parent link, snapshot ID, diff baseline reference.

- `/worlds archive <world_id>`
  - **Output:** archival receipt, retention metadata, audit log ID.

- `/worlds export <world_id> [--patch <##>]`
  - **Output:** export zip path, manifest path, checksum, required re-auth status.

- `/patch start <#>`
  - **Output:** patch workspace scaffold, checklist, dependency validation result.

- `/patch status [<#>]`
  - **Output:** status board with task completion, blockers, artifact readiness.

- `/patch close <#>`
  - **Output:** closure decision (pass/fail), missing gates (if any), release-ready marker.

- `/debug validate_schema`
  - **Output:** schema validation report (pass/fail, violations, migration hints).

- `/debug run_tests [--suite <name>]`
  - **Output:** suite summary, pass/fail counts, flaky-test indicator, report paths.

- `/debug profile_webgl`
  - **Output:** FPS/frame-time/memory/draw-call report against budget targets.

- `/debug export_build`
  - **Output:** build artifact paths, build metadata, checksum manifest.

- `/debug diff_worlds <a> <b>`
  - **Output:** structural/content diff report + compatibility warnings.

- `/release notes <#>`
  - **Output:** generated release notes markdown + unresolved placeholders.

- `/release bundle <#>`
  - **Output:** bundled zip path, manifest summary, included artifact list.

- `/release checksum <#>`
  - **Output:** sha256 manifest and verification status (matching/mismatch).
