from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import DeviceDefinition


class DeviceRegistry:
    def __init__(self, definitions_file: Path) -> None:
        self.definitions_file = definitions_file
        self._definitions: Dict[str, DeviceDefinition] = {}
        self._load()

    def _load(self) -> None:
        data = json.loads(self.definitions_file.read_text())
        for raw in data["devices"]:
            definition = DeviceDefinition(**raw)
            self._definitions[definition.type_id] = definition

    def get(self, type_id: str) -> DeviceDefinition:
        return self._definitions[type_id]

    def all(self) -> List[DeviceDefinition]:
        return list(self._definitions.values())

    def add(self, payload: dict) -> DeviceDefinition:
        definition = DeviceDefinition(**payload)
        self._definitions[definition.type_id] = definition
        self.save()
        return definition

    def save(self) -> None:
        payload = {"devices": [d.__dict__ for d in self._definitions.values()]}
        self.definitions_file.write_text(json.dumps(payload, indent=2))


class PluginRegistry:
    def __init__(self, apps_file: Path, modules_file: Path) -> None:
        self.apps_file = apps_file
        self.modules_file = modules_file
        self.apps = json.loads(apps_file.read_text())["apps"]
        self.modules = json.loads(modules_file.read_text())["modules"]

    def register_app(self, app: dict) -> None:
        self.apps.append(app)
        self.apps_file.write_text(json.dumps({"apps": self.apps}, indent=2))

    def register_module(self, module: dict) -> None:
        self.modules.append(module)
        self.modules_file.write_text(json.dumps({"modules": self.modules}, indent=2))

    def app_names(self) -> List[str]:
        return [a["name"] for a in self.apps]
