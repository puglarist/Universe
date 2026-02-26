from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set

from .schema import ServerMode


@dataclass
class AccessController:
    role_permissions: Dict[str, Set[str]] = field(
        default_factory=lambda: {
            "admin": {"read", "write_canonical", "write_lab", "schema"},
            "mod": {"read", "write_lab"},
            "viewer": {"read"},
        }
    )
    mod_namespaces: Dict[str, str] = field(default_factory=dict)

    def register_mod(self, mod_id: str, namespace: str) -> None:
        self.mod_namespaces[mod_id] = namespace

    def can_write(self, role: str, server_mode: ServerMode) -> bool:
        perms = self.role_permissions.get(role, set())
        if server_mode == ServerMode.CANONICAL:
            return "write_canonical" in perms
        return "write_lab" in perms or "write_canonical" in perms

    def enforce_namespace(self, actor_id: str, namespace: str, role: str) -> None:
        if role == "admin":
            return
        actor_namespace = self.mod_namespaces.get(actor_id)
        if actor_namespace is None or actor_namespace != namespace:
            raise PermissionError("Namespace isolation violation")
