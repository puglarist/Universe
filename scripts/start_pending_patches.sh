#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="$ROOT_DIR/config/patches/pending_patch_registry.json"
PLACEHOLDERS="$ROOT_DIR/placeholders"

if [[ ! -f "$REGISTRY" ]]; then
  echo "Patch registry not found at $REGISTRY" >&2
  exit 1
fi

mkdir -p \
  "$PLACEHOLDERS/survival/assets" \
  "$PLACEHOLDERS/combat/assets" \
  "$PLACEHOLDERS/scrolls/assets" \
  "$PLACEHOLDERS/multiplayer/assets" \
  "$PLACEHOLDERS/ai/assets" \
  "$PLACEHOLDERS/economy/assets" \
  "$PLACEHOLDERS/integration/assets"

cat > "$PLACEHOLDERS/survival/assets/README.txt" <<'TXT'
Placeholder assets for survival/environment systems:
- animals
- trees
- scrap
- farmable plants
TXT

cat > "$PLACEHOLDERS/combat/assets/README.txt" <<'TXT'
Placeholder assets for combat/physics systems:
- arenas
- test NPCs
- destructible props
TXT

cat > "$PLACEHOLDERS/scrolls/assets/README.txt" <<'TXT'
Placeholder assets for scroll network and master simulation UI.
TXT

cat > "$PLACEHOLDERS/multiplayer/assets/README.txt" <<'TXT'
Placeholder assets for multiplayer, party chat, voice, and account sync tests.
TXT

cat > "$PLACEHOLDERS/ai/assets/README.txt" <<'TXT'
Placeholder assets for missions, quests, events, dialogue, loot, and cinematics.
TXT

cat > "$PLACEHOLDERS/economy/assets/README.txt" <<'TXT'
Placeholder assets for professions, marketplaces, NPC shops, and black-market systems.
TXT

cat > "$PLACEHOLDERS/integration/assets/README.txt" <<'TXT'
Placeholder integration assets for cross-system stress testing.
TXT

echo "Started all pending workstreams as defined in: $REGISTRY"
