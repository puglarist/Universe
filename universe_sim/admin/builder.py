from __future__ import annotations

from .permissions import require_admin
from ..models import AuditLogEntry, Player
from ..sim import UniverseSim


class BuilderMenu:
    def __init__(self, sim: UniverseSim) -> None:
        self.sim = sim

    @require_admin
    def spawn_device(self, actor: Player, payload: dict):
        device = self.sim.spawn_device(payload["type_id"], actor.player_id, payload.get("overrides"))
        self.sim.log_admin_action(
            AuditLogEntry(
                actor_id=actor.player_id,
                action="spawn_device",
                target=device.device_id,
                location="in-sim",
                metadata={"type": payload["type_id"]},
            )
        )
        return device

    @require_admin
    def create_app_template(self, actor: Player, app: dict) -> None:
        self.sim.plugins.register_app(app)
        self.sim.log_admin_action(
            AuditLogEntry(
                actor_id=actor.player_id,
                action="create_app_template",
                target=app["name"],
                location="in-sim",
                metadata={"permissions": app.get("permissions", [])},
            )
        )

    @require_admin
    def create_os_module(self, actor: Player, module: dict) -> None:
        self.sim.plugins.register_module(module)
        self.sim.log_admin_action(
            AuditLogEntry(
                actor_id=actor.player_id,
                action="create_os_module",
                target=module["name"],
                location="in-sim",
                metadata={"service": module.get("service")},
            )
        )

    @require_admin
    def modify_device(self, actor: Player, device_id: str, *, rename: str | None = None, add_module: str | None = None) -> None:
        device = self.sim.devices[device_id]
        if rename:
            device.cosmetic_skin = rename
        if add_module and add_module not in device.modules:
            device.modules.append(add_module)
        self.sim.log_admin_action(
            AuditLogEntry(
                actor_id=actor.player_id,
                action="modify_device",
                target=device_id,
                location="in-sim",
                metadata={"rename": rename, "add_module": add_module},
            )
        )


class AdminBackendPanel(BuilderMenu):
    """Backend hook parity with the in-sim menu; actions are audited separately."""

    @require_admin
    def create_device_blueprint(self, actor: Player, blueprint: dict) -> None:
        self.sim.device_registry.add(blueprint)
        self.sim.log_admin_action(
            AuditLogEntry(
                actor_id=actor.player_id,
                action="create_device_blueprint",
                target=blueprint["type_id"],
                location="/admin",
                metadata={"name": blueprint["name"]},
            )
        )
