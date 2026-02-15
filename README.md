# Universe

HomeHub should target an iPhone-friendly architecture:

- **Unity is the authoring engine** (visual world design and behavior definition).
- **The PWA is the runtime** (renders and interacts with exported world data).

This avoids Unity WebGL runtime failures on iOS Safari while preserving a rich, game-engine-authored universe.

## Why not run Unity WebGL directly on iPhone?

In practice, Unity WebGL builds are unreliable on iOS due to Safari/WebKit memory and GPU constraints. Typical outcomes on iPhone are white screens, reload loops, or process termination for heavy scenes.

## Recommended architecture

```text
Unity (URP scene authoring)
        ↓ export
world JSON (+ optional meshes/material metadata)
        ↓ load
HomeHub PWA (Three.js/WebGL runtime)
```

## Data contract (example)

Create a world config export from Unity similar to:

```json
{
  "core_radius": 4.2,
  "pulse_speed": 0.4,
  "modules": [
    {"name": "Codex", "orbit": 8, "size": 1.1, "speed": 0.08},
    {"name": "Counseling", "orbit": 10, "size": 1.2, "speed": 0.06},
    {"name": "Dreamworld", "orbit": 13, "size": 1.4, "speed": 0.04}
  ]
}
```

## First concrete Unity setup (scene authoring only)

Use this exact sequence to produce an initial universe layout that HomeHub can render.

### 1) Project setup

1. Install **Unity Hub**.
2. Create project: **3D URP (Universal Render Pipeline)**.
3. Keep scope minimal: one star + a few orbiting module spheres.

### 2) Scene hierarchy

Create the following hierarchy:

```text
UniverseRoot
├─ CoreSun
├─ OrbitRings
│  ├─ Ring_08
│  ├─ Ring_10
│  └─ Ring_13
└─ Modules
   ├─ Codex
   ├─ Counseling
   └─ Dreamworld
```

### 3) Object defaults

- `CoreSun`
  - Sphere at `(0,0,0)`
  - Scale `(4.2,4.2,4.2)`
  - Emissive material (warm color)
- `Codex`
  - Sphere at `(8,0,0)`
  - Scale `(1.1,1.1,1.1)`
- `Counseling`
  - Sphere at `(10,0,0)`
  - Scale `(1.2,1.2,1.2)`
- `Dreamworld`
  - Sphere at `(13,0,0)`
  - Scale `(1.4,1.4,1.4)`

### 4) Orbital behavior parameters (author-time values)

Store or annotate these values per module:

| Module      | Orbit Radius | Size | Angular Speed |
|-------------|--------------|------|---------------|
| Codex       | 8            | 1.1  | 0.08          |
| Counseling  | 10           | 1.2  | 0.06          |
| Dreamworld  | 13           | 1.4  | 0.04          |

### 5) Export target

Do **not** build WebGL yet.

Instead, export a JSON file consumed by HomeHub's web renderer. Unity remains the map editor; HomeHub remains the runtime shell.

## HomeHub runtime responsibilities

- Render core + modules in WebGL (Three.js recommended).
- Animate orbits and core pulse from exported parameters.
- Handle interaction and overlay UI without tearing down the world scene.
- Persist system state outside Unity (local storage and/or backend).

## Suggested next milestone

Implement a Unity export script that writes `core.json` from scene objects under `UniverseRoot`, then wire HomeHub to load and render that file at startup.
