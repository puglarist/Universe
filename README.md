# Universe

HomeHub as a **remote spatial operating system**: the phone is a thin client (viewer + controller), and the GPU server does simulation/rendering.

## Goal

Run an interactive, ultra-realistic universe experience on weak devices (iPhone/Safari/Firefox) by using cloud rendering instead of on-device 3D rendering.

## System Architecture

```text
Phone (HomeHub PWA)
  - UI/menu/voice
  - controller + keyboard/mouse input
  - decodes interactive video stream
          |
          | WebRTC (low-latency A/V + data channels)
          v
RunPod GPU Pod
  - Unity/Unreal runtime
  - real-time rendering + physics simulation
  - stream encoder (NVENC/AV1/H264)
  - input bridge -> game engine
          |
          | HTTPS API / gRPC / message bus
          v
AI Services (Hugging Face + custom backend)
  - assistant reasoning
  - retrieval + memory indexing
  - perception modules (optional)
```

## Responsibility Split

### HomeHub PWA (client)
- Session management + auth token handling
- Render streamed video in browser
- Relay input events (gamepad/touch/keyboard/mouse)
- Show overlays: HUD, chat, module launcher, latency meter
- Optional local mic capture for voice interaction

### RunPod GPU Runtime (server)
- Host 3D world and simulation loop
- Render scene frames at 60 FPS target
- Encode and stream via WebRTC
- Consume input data channel and apply to player/camera
- Expose telemetry: FPS, RTT, packet loss, queue delay

### AI Layer (Hugging Face-backed)
- Handle natural-language commands
- Query memory/index data stores
- Return world actions/events (e.g., spawn module)
- Keep this decoupled from render transport layer

## Minimal Deployable Stack (MVP)

1. **HomeHub PWA shell**
   - Routes: `/` (launcher), `/session/:id` (stream view)
   - Connect button triggers signaling handshake
2. **Signaling service**
   - WebSocket endpoint for SDP/ICE exchange
   - Issues short-lived session tokens
3. **RunPod WebRTC worker**
   - Container with GPU access + WebRTC stack
   - Publishes video track + data channel
4. **Simple 3D scene**
   - Orbit camera + single “core sun” object
   - Basic movement and lighting
5. **Input relay**
   - Browser Gamepad API + keyboard/touch mapping
   - Data channel messages to runtime

## RunPod Container Components

- Base image with NVIDIA runtime support
- Engine runtime binary (Unity headless player build or Unreal packaged build)
- WebRTC gateway process (GStreamer/Pion/Janus-based bridge)
- TURN/STUN configuration for NAT traversal
- Metrics sidecar (Prometheus exporter optional)

## Suggested API Contracts

### Signaling
- `POST /sessions` -> `{ sessionId, token, wsUrl }`
- `WS /signal/:sessionId` for SDP offer/answer + ICE candidates

### Data Channel Messages
- `input.move` `{ x, y }`
- `input.look` `{ dx, dy }`
- `input.action` `{ type: "interact" | "menu" | "boost" }`
- `system.ping` `{ t }` / `system.pong` `{ t }`

### AI Command Gateway
- `POST /ai/command` `{ sessionId, text }`
- Response includes actionable world events:
  - `{ action: "spawn_module", module: "counseling", position: [x,y,z] }`

## Phased Build Plan

### Phase 1 — Connection Proof
- PWA page displays remote stream
- End-to-end WebRTC from RunPod to iPhone browser
- Latency and reconnect indicators visible

### Phase 2 — Interaction Proof
- Reliable input relay over data channel
- Camera/world responds to gamepad + touch
- Target latency: ~40–80 ms under good network conditions

### Phase 3 — Visual Upgrade
- Replace simple scene with richer sun/space environment
- Add dynamic lighting, particles, atmospheric effects

### Phase 4 — AI Layer Integration
- Add assistant command endpoint
- Bind commands to in-world events and modules

## Why this works on Safari/Firefox

Browsers are decoding an interactive video stream rather than executing heavy 3D workloads. This bypasses mobile GPU limitations while preserving real-time control.

## Immediate Next Steps

1. Build signaling server and test local browser-to-pod handshake
2. Deploy RunPod container with sample stream output
3. Implement PWA stream page + input channel events
4. Validate on iPhone Safari with a controller
5. Add scene complexity only after stable transport + control
