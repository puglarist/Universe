# Universe

## HomeHub Core: Agent + Simulation Bootstrap

This repository now includes a minimal **HomeHub Core** backend that implements the immediate next step from the linear update:

- Agent communication layer
- Agent task protocol
- Command routing from HomeHub input to Hugging Face inference
- World-state mutation based on agent actions

## Architecture

- **PWA / Client** sends user commands to `POST /api/command`
- **Agent Orchestrator** selects one of four initial roles:
  - Architect
  - Archivist
  - Counselor
  - Operator
- **Hugging Face Client** calls inference endpoint (or local mock mode when `HF_API_KEY` is not set)
- **World Store** applies produced actions and stores environment/module/memory updates

## API Surface

- `GET /health` → service status
- `GET /api/agents` → registered initial agents
- `GET /api/world` → current simulation world snapshot
- `POST /api/command` → execute a command through role selection + inference + world action

### Command Payload

```json
{
  "user_id": "u-123",
  "session_id": "ios-pwa-1",
  "command": "Build a coastal terrain zone for the new memory district",
  "context": {
    "input": "touch"
  }
}
```

### Response Outline

- Selected role
- Agent reasoning output
- Generated actions
- Updated world snapshot

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn homehub_core.main:app --reload --port 8000
```

## Hugging Face Configuration

Set environment variables for live inference:

- `HF_API_KEY`
- `HF_INFERENCE_URL` (optional override, defaults to Hugging Face Inference API)
- `HF_DEFAULT_MODEL` (default: `google/flan-t5-base`)

Without `HF_API_KEY`, the system runs in mock inference mode for local dev/testing.
