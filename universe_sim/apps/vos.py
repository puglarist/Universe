from __future__ import annotations

from dataclasses import dataclass

from ..sim import UniverseSim


@dataclass
class VOSStatus:
    battery: int
    temperature: int
    storage_used: int
    storage_capacity: int
    time_label: str


class VOSShell:
    def __init__(self, sim: UniverseSim) -> None:
        self.sim = sim

    def boot(self, device_id: str, login_required: bool = False) -> str:
        self.sim.open_device(device_id)
        return "login" if login_required else "desktop"

    def desktop(self, device_id: str) -> dict:
        device = self.sim.devices[device_id]
        return {
            "dock": self.sim.plugins.app_names(),
            "notifications": device.state.notifications,
            "status": self.status_bar(device_id).__dict__,
            "directories": ["/home", "/apps", "/world_exports", "/logs"],
        }

    def status_bar(self, device_id: str) -> VOSStatus:
        d = self.sim.devices[device_id]
        return VOSStatus(
            battery=d.battery_level,
            temperature=d.heat_level,
            storage_used=d.storage_used,
            storage_capacity=d.storage_capacity,
            time_label="sim-time",
        )

    def suspend(self, device_id: str) -> None:
        self.sim.close_device(device_id)
