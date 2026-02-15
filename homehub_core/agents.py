from __future__ import annotations

from uuid import uuid4

from homehub_core.hf_client import HuggingFaceClient
from homehub_core.models import AgentAction, AgentResult, AgentTask, AgentRole


ROLE_CONFIG: dict[AgentRole, dict[str, list[str]]] = {
    "architect": {
        "memory_scope": ["terrain", "layout_history", "module_map"],
        "action_set": ["terrain.create", "structure.spawn"],
    },
    "archivist": {
        "memory_scope": ["logs", "notes", "datasets"],
        "action_set": ["memory.anchor", "structure.spawn"],
    },
    "counselor": {
        "memory_scope": ["wellness_records", "conversation_history"],
        "action_set": ["wellness.respond", "memory.anchor"],
    },
    "operator": {
        "memory_scope": ["permissions", "runtime_state", "task_queue"],
        "action_set": ["system.execute", "structure.spawn"],
    },
}


class AgentOrchestrator:
    def __init__(self, hf_client: HuggingFaceClient) -> None:
        self.hf_client = hf_client

    def select_role(self, command: str) -> AgentRole:
        lowered = command.lower()
        if any(token in lowered for token in ["terrain", "build", "world", "zone"]):
            return "architect"
        if any(token in lowered for token in ["log", "archive", "dataset", "memory"]):
            return "archivist"
        if any(token in lowered for token in ["wellness", "mood", "counsel", "talk"]):
            return "counselor"
        return "operator"

    async def run(self, role: AgentRole, objective: str, world_snapshot: dict) -> AgentResult:
        config = ROLE_CONFIG[role]
        task = AgentTask(
            id=str(uuid4()),
            role=role,
            objective=objective,
            memory_scope=config["memory_scope"],
            action_set=config["action_set"],
            world_snapshot=world_snapshot,
        )

        prompt = (
            f"Role: {task.role}\n"
            f"Objective: {task.objective}\n"
            f"ActionSet: {task.action_set}\n"
            f"World: {task.world_snapshot}\n"
            "Return concise planning guidance for the role."
        )
        inference = await self.hf_client.infer(prompt)
        output = str(inference["output"])

        action = self._build_action(role, objective)
        return AgentResult(
            task_id=task.id,
            role=role,
            summary=f"{role} handled objective",
            reasoning=output,
            actions=[action],
        )

    def _build_action(self, role: AgentRole, objective: str) -> AgentAction:
        if role == "architect":
            return AgentAction(
                type="terrain.create",
                payload={"zone": "new-zone", "intent": objective, "seed": "earth-v1"},
            )
        if role == "archivist":
            return AgentAction(
                type="memory.anchor",
                payload={"label": "new-memory-location", "source": objective},
            )
        if role == "counselor":
            return AgentAction(
                type="wellness.respond",
                payload={"message": "Support module updated", "source": objective},
            )
        return AgentAction(
            type="system.execute",
            payload={"operation": "command_dispatch", "command": objective},
        )
