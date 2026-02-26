from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Dict, List, Optional

from .models import AuditLogEntry, Device, Player, VOSFile, Vehicle
from .registry import DeviceRegistry, PluginRegistry


class UniverseSim:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.device_registry = DeviceRegistry(root / "universe_sim/data/devices.json")
        self.plugins = PluginRegistry(root / "universe_sim/data/apps.json", root / "universe_sim/data/modules.json")
        self.devices: Dict[str, Device] = {}
        self.vehicles: Dict[str, Vehicle] = {}
        self.audit_log: List[AuditLogEntry] = []

    def spawn_device(self, type_id: str, owner_id: Optional[str] = None, overrides: Optional[dict] = None) -> Device:
        definition = self.device_registry.get(type_id)
        device = Device(definition=definition, owner_id=owner_id)
        if overrides:
            for k, v in overrides.items():
                setattr(device, k, v)
        self.devices[device.device_id] = device
        return device

    def pickup(self, player: Player, device_id: str) -> None:
        if player.carry_slot is None:
            player.carry_slot = device_id
        elif len(player.inventory.items) < player.inventory.capacity:
            player.inventory.items.append(device_id)
        else:
            raise ValueError("No carry or inventory space")

    def place_on_surface(self, player: Player, device_id: str, surface: str) -> str:
        if player.carry_slot == device_id:
            player.carry_slot = None
            return f"Placed {device_id} on {surface}"
        if device_id in player.inventory.items:
            player.inventory.items.remove(device_id)
            return f"Placed {device_id} on {surface}"
        raise ValueError("Device not held")

    def store_in_vehicle(self, player: Player, device_id: str, vehicle: Vehicle) -> None:
        if player.carry_slot == device_id:
            player.carry_slot = None
        elif device_id in player.inventory.items:
            player.inventory.items.remove(device_id)
        else:
            raise ValueError("Device not held")
        if len(vehicle.cargo_inventory.items) >= vehicle.cargo_inventory.capacity:
            raise ValueError("Vehicle cargo full")
        vehicle.cargo_inventory.items.append(device_id)

    def mount_to_vehicle(self, player: Player, device_id: str, vehicle: Vehicle, mount_point: str) -> None:
        if "mount_kit" not in self.devices[device_id].modules:
            raise ValueError("Mount bracket item required")
        if vehicle.mount_points[mount_point] is not None:
            raise ValueError("Mount point occupied")
        if player.carry_slot == device_id:
            player.carry_slot = None
        elif device_id in player.inventory.items:
            player.inventory.items.remove(device_id)
        vehicle.mount_points[mount_point] = device_id

    def retrieve_from_vehicle(self, player: Player, device_id: str, vehicle: Vehicle) -> None:
        if player.carry_slot is not None:
            raise ValueError("Carry slot occupied")
        if device_id in vehicle.cargo_inventory.items:
            vehicle.cargo_inventory.items.remove(device_id)
            player.carry_slot = device_id
            return
        for point, mounted in vehicle.mount_points.items():
            if mounted == device_id:
                vehicle.mount_points[point] = None
                player.carry_slot = device_id
                return
        raise ValueError("Device not found in vehicle")

    def open_device(self, device_id: str) -> None:
        d = self.devices[device_id]
        d.state.power_on = True
        d.state.open_state = True
        d.state.suspended = False
        d.battery_level = max(0, d.battery_level - 1)

    def close_device(self, device_id: str) -> None:
        d = self.devices[device_id]
        d.state.open_state = False
        d.state.suspended = True

    def write_file(self, device_id: str, path: str, file_type: str, content: str) -> None:
        d = self.devices[device_id]
        size = len(content.encode("utf-8"))
        existing = d.files.get(path)
        existing_size = existing.size if existing else 0
        projected = d.storage_used - existing_size + size
        if projected > d.storage_capacity:
            raise ValueError("Storage full")
        d.files[path] = VOSFile(path=path, file_type=file_type, content=content, size=size)
        d.storage_used = projected

    def launch_app(self, device_id: str, app_name: str) -> None:
        if app_name not in self.plugins.app_names():
            raise ValueError("Unknown app")
        d = self.devices[device_id]
        if app_name not in d.state.active_apps:
            d.state.active_apps.append(app_name)

    def save_world(self, path: Path) -> None:
        payload = {
            "devices": {
                k: {
                    "definition": asdict(v.definition),
                    "owner_id": v.owner_id,
                    "firmware_version": v.firmware_version,
                    "os_version": v.os_version,
                    "network_mode": v.network_mode,
                    "battery_level": v.battery_level,
                    "heat_level": v.heat_level,
                    "durability": v.durability,
                    "storage_used": v.storage_used,
                    "files": {fp: asdict(f) for fp, f in v.files.items()},
                    "state": asdict(v.state),
                    "permissions": v.permissions,
                    "modules": v.modules,
                    "cosmetic_skin": v.cosmetic_skin,
                    "device_id": v.device_id,
                }
                for k, v in self.devices.items()
            }
        }
        path.write_text(json.dumps(payload, indent=2))

    def load_world(self, path: Path) -> None:
        payload = json.loads(path.read_text())
        self.devices = {}
        for device_id, raw in payload["devices"].items():
            device = self.spawn_device(raw["definition"]["type_id"], raw["owner_id"])
            device.device_id = raw["device_id"]
            device.firmware_version = raw["firmware_version"]
            device.os_version = raw["os_version"]
            device.network_mode = raw["network_mode"]
            device.battery_level = raw["battery_level"]
            device.heat_level = raw["heat_level"]
            device.durability = raw["durability"]
            device.storage_used = raw["storage_used"]
            device.files = {fp: VOSFile(**f) for fp, f in raw["files"].items()}
            device.state.power_on = raw["state"]["power_on"]
            device.state.open_state = raw["state"]["open_state"]
            device.state.suspended = raw["state"]["suspended"]
            device.state.active_apps = raw["state"]["active_apps"]
            device.state.notifications = raw["state"]["notifications"]
            device.permissions = raw["permissions"]
            device.modules = raw["modules"]
            device.cosmetic_skin = raw["cosmetic_skin"]
            self.devices.pop(next(iter([k for k, v in self.devices.items() if v is device]), device_id), None)
            self.devices[device_id] = device

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicles[vehicle.vehicle_id] = vehicle

    def charge_from_vehicle(self, device_id: str, has_adapter: bool) -> None:
        if not has_adapter:
            return
        d = self.devices[device_id]
        d.battery_level = min(100, d.battery_level + 10)

    def log_admin_action(self, entry: AuditLogEntry) -> None:
        self.audit_log.append(entry)
