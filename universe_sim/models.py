from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class DeviceDefinition:
    type_id: str
    name: str
    weight: float
    size: int
    durability: int
    battery_capacity: int
    storage_capacity: int
    supports_hinge: bool
    mount_compatible: bool


@dataclass
class VOSFile:
    path: str
    file_type: str
    content: str
    size: int


@dataclass
class DeviceState:
    power_on: bool = False
    open_state: bool = False
    suspended: bool = False
    active_apps: List[str] = field(default_factory=list)
    notifications: List[str] = field(default_factory=list)


@dataclass
class Device:
    definition: DeviceDefinition
    owner_id: Optional[str] = None
    firmware_version: str = "1.0.0"
    os_version: str = "VOS-1.0"
    network_mode: str = "offline"
    battery_level: int = 100
    heat_level: int = 0
    durability: Optional[int] = None
    storage_used: int = 0
    files: Dict[str, VOSFile] = field(default_factory=dict)
    state: DeviceState = field(default_factory=DeviceState)
    permissions: Dict[str, bool] = field(default_factory=lambda: {"admin_override": False, "owner_lock": False})
    modules: List[str] = field(default_factory=list)
    cosmetic_skin: str = "default"
    device_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.durability is None:
            self.durability = self.definition.durability

    @property
    def storage_capacity(self) -> int:
        extra = 256 if "extra_storage" in self.modules else 0
        return self.definition.storage_capacity + extra


@dataclass
class Inventory:
    capacity: int
    items: List[str] = field(default_factory=list)


@dataclass
class Vehicle:
    vehicle_id: str
    cargo_inventory: Inventory = field(default_factory=lambda: Inventory(capacity=10))
    mount_points: Dict[str, Optional[str]] = field(
        default_factory=lambda: {"passenger_seat": None, "dash_mount": None, "trunk_rack": None}
    )


@dataclass
class Player:
    player_id: str
    is_admin: bool = False
    carry_slot: Optional[str] = None
    inventory: Inventory = field(default_factory=lambda: Inventory(capacity=6))


@dataclass
class AuditLogEntry:
    actor_id: str
    action: str
    target: str
    location: str
    metadata: Dict[str, Any]
    simulation_only: bool = True
