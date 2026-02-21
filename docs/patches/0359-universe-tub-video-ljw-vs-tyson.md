# Patch 359 - Universe Tub Video / Little Jerry Wayne vs Mike Tyson

## Vision
Build an emergent social streaming layer inside **Universe Tub** where players can upload, broadcast, and replay chaotic avatar battles (including **Little Jerry Wayne vs Mike Tyson** scenarios) as dynamic, AI-edited media.

---

## Scope Summary
Patch 359 introduces a full **capture -> generate -> edit -> publish -> interact -> learn** loop:

1. Capture PvP and environmental events from live matches.
2. Generate emergent clips and highlights using AI-driven sequencing.
3. Publish videos to Universe Tub as uploads, live streams, and replay reels.
4. Enable social interaction (likes, comments, shares, procedural challenges).
5. Feed all telemetry into Codex/meta-learning for future clip generation.

---

## Core Systems

### 1) Universe Tub Video Pipeline

**Modes**
- **Upload**: Player uploads a locally recorded clip package.
- **Live**: Match is streamed in real-time to a Universe Tub channel.
- **Replay**: AI assembles highlights from captured combat telemetry.

**Pipeline Stages**
1. `FightCaptureService` records combat and world events.
2. `EmergentClipBuilder` converts event streams into candidate beats.
3. `AIDirector` scores beats (impact, novelty, chaos, style diversity).
4. `ProceduralEditor` builds final timeline (cuts, replays, angle swaps).
5. `UniverseTubPublisher` posts content and metadata.

---

### 2) Emergent Combat Coverage

Patch 359 guarantees all current combat styles are represented in generated media:
- **Puglar**
- **Timmy MMA**
- **Figure It Out**
- **Stormfight**

**Selection Rules**
- Prefer clips with style transitions and counters.
- Weight unique interactions (throws into hazards, prop knockbacks).
- Promote rounds with environmental chain reactions.

---

### 3) Social + Audience Layer

Universe Tub video entities now support:
- `likes`
- `shares`
- `comments`
- `reactionBursts` (crowd taunts/cheers)
- `challengeSeeds` (procedural viewer challenges)

**AI Commentary Tracks**
- Real-time crowd hype lines.
- Rivalry-specific taunts (e.g., Little Jerry Wayne vs Tyson archetype).
- Momentum-sensitive reactions (comeback spikes, upset moments).

---

### 4) Team/Crew Integration

Video generation supports:
- Team tags (`little_jerry_wayne_team`, `mike_tyson_style_team`, custom crews).
- Crew combo highlights.
- NPC and dog participation in event timelines.

**Crew-Aware Highlights**
- Combos are grouped into "crew moments."
- AI produces alternate edits emphasizing teamwork or solo clutch plays.

---

### 5) Environment-Aware Capture

Matches include:
- Multi-level arenas
- Vertical traversal events
- Destructible props
- Dynamic hazards

**Editor Effects**
- Slow motion at major destruction beats.
- Replay angles for ring-outs/falls/collisions.
- Event layering to ensure each produced clip is unique.

---

### 6) Codex Meta-Learning Integration

Patch logs every video-relevant signal:
- Combat sequences
- Environmental interactions
- Emergent combo graphs
- Viewer engagement events

**Learning Loop**
1. Persist logs to `VideoCombatLog`.
2. Build feature vectors for clip quality and replay value.
3. Retrain ranking weights for future highlight generation.
4. Spawn new procedural scenarios for viewer challenge content.

---

## Data Contracts

### Event: `CombatVideoEvent`
```json
{
  "matchId": "m_4582",
  "timestampMs": 128450,
  "actorId": "avatar_ljw",
  "targetId": "avatar_tyson",
  "combatStyle": "Puglar",
  "eventType": "heavy_hit",
  "arenaZone": "catwalk_upper",
  "propState": "crate_destroyed",
  "crewTag": "little_jerry_wayne_team",
  "noveltyScore": 0.91
}
```

### Entity: `UniverseTubVideo`
```json
{
  "videoId": "utv_90031",
  "mode": "replay",
  "title": "Little Jerry Wayne vs Mike Tyson - Catwalk Chaos",
  "participants": ["avatar_ljw", "avatar_tyson", "npc_ref_07", "dog_02"],
  "stylesSeen": ["Puglar", "Stormfight"],
  "crewMoments": 4,
  "hazardEvents": 3,
  "likes": 0,
  "shares": 0,
  "comments": [],
  "challengeSeed": "seed_55A2"
}
```

---

## Service Interfaces (Reference)

```ts
interface FightCaptureService {
  beginCapture(matchId: string): void;
  recordEvent(event: CombatVideoEvent): void;
  endCapture(matchId: string): CaptureBundle;
}

interface EmergentClipBuilder {
  buildCandidates(bundle: CaptureBundle): ClipCandidate[];
}

interface AIDirector {
  rank(candidates: ClipCandidate[], context: DirectorContext): RankedClip[];
}

interface ProceduralEditor {
  assembleTimeline(input: RankedClip[]): RenderTimeline;
}

interface UniverseTubPublisher {
  publishVideo(video: UniverseTubVideo, timeline: RenderTimeline): PublishedVideo;
  startLiveStream(channelId: string, matchId: string): LiveSession;
}
```

---

## Iteration Mapping

### Iteration 1 - Core Video Mechanics
- Added upload/live/playback model support.
- Added AI-generated highlight production from PvP telemetry.
- Added avatar customization and stage/prop/style embedding in media metadata.

### Iteration 2 - Emergent Combat in Video
- Enabled all combat styles in generated and live footage.
- Added dynamic sequence scoring and key-moment extraction.
- Added replay clips for strategy and environment interaction visibility.

### Iteration 3 - Audience & Social Features
- Added AI commentary and crowd-reaction channels.
- Added likes, shares, comments.
- Added procedural challenge seed generation from video events.

### Iteration 4 - Team & Crew Integration
- Added crew identity and combo-aware edits.
- Added NPC and dog participant support.
- Added crew-performance adaptive highlight weighting.

### Iteration 5 - Environmental Video Integration
- Added multi-level/destructible/hazard event capture.
- Added environmental emphasis passes in replay rendering.
- Added uniqueness guarantees through procedural edit variability.

### Iteration 6 - Codex & Meta-Learning
- Added structured logging of capture and engagement signals.
- Added AI feedback loop for future reel quality.
- Added compatibility target with existing Universe Tub streaming/replay stack.

---

## Acceptance Criteria

- Players can upload, live stream, and replay Universe Tub battle videos.
- Generated clips include emergent combat, crews, NPCs/dogs, and environment events.
- AI commentary and social interactions are active on published videos.
- Procedural challenge seeds are attached to eligible clips.
- Codex logs all capture/edit/publish/engagement events for future generation.

---

## Outcome

Patch 359 fully integrates a replayable, social, AI-directed video ecosystem into Universe Tub, enabling dynamic showcase battles such as **Little Jerry Wayne vs Mike Tyson** while continuously evolving future content via Codex meta-learning.
