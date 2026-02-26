from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, Mapping


class ServerMode(str, Enum):
    CANONICAL = "canonical"
    LAB = "lab"


CORE_NODE_TYPES: FrozenSet[str] = frozenset(
    {
        "entity",
        "device",
        "timeline_branch",
        "law",
        "court_case",
        "faction",
        "blueprint",
        "mod",
        "chrono_message",
    }
)

CORE_EDGE_TYPES: FrozenSet[str] = frozenset(
    {
        "OWNS",
        "CREATED_AT",
        "DERIVED_FROM",
        "BRANCH_OF",
        "REFERENCES",
        "INFLUENCES",
        "TESTED_IN",
    }
)


@dataclass(frozen=True)
class NodeRecord:
    node_id: str
    node_type: str
    namespace: str
    data: Mapping[str, Any]
    version: int
    timeline_id: str
    branch_id: str
    server_mode: ServerMode
    tick: int
    created_by: str
    content_hash: str


@dataclass(frozen=True)
class EdgeRecord:
    edge_type: str
    source_id: str
    target_id: str
    tick: int
    timeline_id: str
    branch_id: str
    server_mode: ServerMode


@dataclass
class SchemaRegistry:
    node_types: Dict[str, Dict[str, type]] = field(default_factory=dict)
    edge_types: FrozenSet[str] = CORE_EDGE_TYPES

    def register_node_schema(self, node_type: str, schema: Dict[str, type]) -> None:
        self.node_types[node_type] = schema

    def validate_node(self, node_type: str, data: Mapping[str, Any]) -> None:
        if node_type not in self.node_types and node_type not in CORE_NODE_TYPES:
            raise ValueError(f"Unknown node type: {node_type}")
        schema = self.node_types.get(node_type, {})
        for key, expected_type in schema.items():
            if key not in data:
                raise ValueError(f"Missing required field: {key}")
            if not isinstance(data[key], expected_type):
                raise TypeError(f"Field {key} should be {expected_type.__name__}")

    def validate_edge_type(self, edge_type: str) -> None:
        if edge_type not in self.edge_types:
            raise ValueError(f"Unknown edge type: {edge_type}")
