from __future__ import annotations

from fastapi import FastAPI

from homehub_core.agents import AgentOrchestrator
from homehub_core.hf_client import HuggingFaceClient
from homehub_core.models import ClientCommand
from homehub_core.world import WorldStore

app = FastAPI(title="HomeHub Core", version="0.1.0")

world_store = WorldStore()
orchestrator = AgentOrchestrator(hf_client=HuggingFaceClient())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/agents")
async def list_agents() -> dict:
    return {
        "agents": [
            {"role": "architect", "status": "ready"},
            {"role": "archivist", "status": "ready"},
            {"role": "counselor", "status": "ready"},
            {"role": "operator", "status": "ready"},
        ]
    }


@app.get("/api/world")
async def get_world() -> dict:
    return world_store.snapshot().model_dump()


@app.post("/api/command")
async def post_command(command: ClientCommand) -> dict:
    role = orchestrator.select_role(command.command)
    result = await orchestrator.run(
        role=role,
        objective=command.command,
        world_snapshot=world_store.snapshot().model_dump(),
    )
    world_store.apply_actions(source=role, actions=result.actions)

    return {
        "selected_role": role,
        "result": result.model_dump(),
        "world": world_store.snapshot().model_dump(),
    }
