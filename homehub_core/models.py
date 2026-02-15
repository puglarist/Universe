from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


AgentRole = Literal["architect", "archivist", "counselor", "operator"]


class ClientCommand(BaseModel):
    user_id: str = Field(..., description="Authenticated HomeHub user id")
    session_id: str = Field(..., description="PWA session identifier")
    command: str = Field(..., description="Raw natural-language command from the user")
    context: dict[str, Any] = Field(default_factory=dict)


class AgentTask(BaseModel):
    id: str
    role: AgentRole
    objective: str
    memory_scope: list[str] = Field(default_factory=list)
    action_set: list[str] = Field(default_factory=list)
    world_snapshot: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentAction(BaseModel):
    type: Literal[
        "terrain.create",
        "structure.spawn",
        "memory.anchor",
        "wellness.respond",
        "system.execute",
    ]
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    task_id: str
    role: AgentRole
    summary: str
    reasoning: str
    actions: list[AgentAction]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WorldEvent(BaseModel):
    id: str
    type: str
    source: str
    payload: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WorldState(BaseModel):
    environment: dict[str, Any] = Field(default_factory=dict)
    modules: list[dict[str, Any]] = Field(default_factory=list)
    memory_locations: list[dict[str, Any]] = Field(default_factory=list)
    events: list[WorldEvent] = Field(default_factory=list)
