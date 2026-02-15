# Unity Setup Checklist (Patch 0)

## Recommended Baseline
- Unity LTS version compatible with:
  - WebGL
  - iOS (Xcode toolchain)
  - Desktop (Windows/macOS as needed)
- Rendering pipeline:
  - URP (recommended baseline for cross-platform performance), or
  - HDRP (if desktop-first high-fidelity target)

## Steps
1. Install Unity Hub + target Unity LTS.
2. Add build support modules:
   - WebGL Build Support
   - iOS Build Support
3. Create project and configure render pipeline package.
4. Create `EmptyWorld` scene with:
   - Main camera
   - Directional light
   - Plane + cube placeholder
   - Rigidbody/collider sample for physics sanity check
5. Set quality and GPU/performance defaults.
6. Save and set `EmptyWorld` as startup scene.

## Verification
- [ ] Scene loads from clean launch.
- [ ] Camera movement works.
- [ ] Physics interaction visible with placeholders.
- [ ] WebGL build completes.
- [ ] iOS export completes.
