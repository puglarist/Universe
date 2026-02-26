from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Dict, Iterable, List, Optional, Tuple

from .schema import EdgeRecord, NodeRecord, SchemaRegistry, ServerMode
from .security import AccessController


@dataclass
class StructuredKnowledgeGraph:
    registry: SchemaRegistry = field(default_factory=SchemaRegistry)
    access: AccessController = field(default_factory=AccessController)
    nodes: Dict[str, List[NodeRecord]] = field(default_factory=lambda: defaultdict(list))
    edges: List[EdgeRecord] = field(default_factory=list)
    audit_log: List[str] = field(default_factory=list)

    def _hash_payload(self, node_id: str, payload: dict, tick: int) -> str:
        text = f"{node_id}|{tick}|{sorted(payload.items())}"
        return sha256(text.encode("utf-8")).hexdigest()

    def upsert_node(
        self,
        *,
        actor_id: str,
        role: str,
        node_id: str,
        node_type: str,
        namespace: str,
        data: dict,
        timeline_id: str,
        branch_id: str,
        server_mode: ServerMode,
        tick: int,
    ) -> NodeRecord:
        if not self.access.can_write(role, server_mode):
            raise PermissionError("Write denied for server mode")
        self.access.enforce_namespace(actor_id, namespace, role)
        self.registry.validate_node(node_type, data)

        history = self.nodes[node_id]
        version = history[-1].version + 1 if history else 1
        record = NodeRecord(
            node_id=node_id,
            node_type=node_type,
            namespace=namespace,
            data=data,
            version=version,
            timeline_id=timeline_id,
            branch_id=branch_id,
            server_mode=server_mode,
            tick=tick,
            created_by=actor_id,
            content_hash=self._hash_payload(node_id, data, tick),
        )
        history.append(record)
        self.audit_log.append(f"upsert_node:{node_id}:v{version}:t{tick}:{server_mode.value}")
        return record

    def add_edge(
        self,
        *,
        edge_type: str,
        source_id: str,
        target_id: str,
        timeline_id: str,
        branch_id: str,
        server_mode: ServerMode,
        tick: int,
    ) -> EdgeRecord:
        self.registry.validate_edge_type(edge_type)
        edge = EdgeRecord(
            edge_type=edge_type,
            source_id=source_id,
            target_id=target_id,
            timeline_id=timeline_id,
            branch_id=branch_id,
            server_mode=server_mode,
            tick=tick,
        )
        self.edges.append(edge)
        self.audit_log.append(f"add_edge:{edge_type}:{source_id}->{target_id}:t{tick}")
        return edge

    def iter_nodes(self) -> Iterable[NodeRecord]:
        for records in self.nodes.values():
            for record in records:
                yield record

    def latest_node(self, node_id: str) -> Optional[NodeRecord]:
        history = self.nodes.get(node_id)
        if not history:
            return None
        return history[-1]

    def export_branch_diff(
        self, *, timeline_id: str, branch_a: str, branch_b: str
    ) -> Tuple[List[NodeRecord], List[NodeRecord]]:
        a_nodes = [n for n in self.iter_nodes() if n.timeline_id == timeline_id and n.branch_id == branch_a]
        b_nodes = [n for n in self.iter_nodes() if n.timeline_id == timeline_id and n.branch_id == branch_b]
        return a_nodes, b_nodes
