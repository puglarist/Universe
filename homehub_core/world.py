from __future__ import annotations

from uuid import uuid4

from homehub_core.models import AgentAction, WorldEvent, WorldState


class WorldStore:
    def __init__(self) -> None:
        self.state = WorldState(
            environment={
                "name": "earth-seed",
                "phase": "phase-1",
                "day_cycle": {"enabled": True, "time": "06:00"},
                "skybox": "temperate",
                "zones": [],
            }
        )

    def snapshot(self) -> WorldState:
        return self.state

    def apply_actions(self, source: str, actions: list[AgentAction]) -> None:
        for action in actions:
            if action.type == "terrain.create":
                self.state.environment.setdefault("zones", []).append(action.payload)
            elif action.type == "structure.spawn":
                self.state.modules.append(action.payload)
            elif action.type == "memory.anchor":
                self.state.memory_locations.append(action.payload)
            elif action.type in {"wellness.respond", "system.execute"}:
                self.state.modules.append({"type": action.type, **action.payload})

            self.state.events.append(
                WorldEvent(
                    id=str(uuid4()),
                    type=action.type,
                    source=source,
                    payload=action.payload,
                )
            )
