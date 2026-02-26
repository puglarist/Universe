# Universe

## PATCH-93: SlyFox MetaWeb Engine + Simulation-Superior Network

This patch introduces a simulation-native **MetaWeb** reference implementation with:

- Structured Knowledge Graph (typed nodes/edges, versioned records, timeline + branch awareness)
- Instant indexing through direct world-event-style upserts
- Timeline-aware query layer with deterministic filtering and sorting
- Reset-server integration that wipes lab data while preserving canonical history
- Role and namespace security controls, canonical write locks, and audit log trails
- MetaWeb Navigator device/admin feature profiles

## Implementation map

- `metaweb/schema.py` — core schemas, core node/edge type catalogs, validation registry
- `metaweb/graph_engine.py` — deterministic graph storage, versioning, edge tracking, audit log
- `metaweb/query.py` — timeline-aware, branch-aware, server-aware query layer
- `metaweb/reset.py` — reset-server lab wipe and report generation
- `metaweb/security.py` — RBAC + namespace isolation
- `metaweb/navigator.py` — in-sim device and admin overlay feature model
- `tests/test_metaweb.py` — CODEx-901/902/903/904/905 functional tests

## Running tests

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```
