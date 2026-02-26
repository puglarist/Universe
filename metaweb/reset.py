from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .graph_engine import StructuredKnowledgeGraph
from .schema import NodeRecord, ServerMode


@dataclass
class ResetReport:
    removed_lab_nodes: int
    removed_lab_edges: int


class ResetServerIntegrator:
    def __init__(self, graph: StructuredKnowledgeGraph) -> None:
        self.graph = graph

    def reset_lab_server(self, timeline_id: str) -> ResetReport:
        removed_nodes = 0
        for node_id in list(self.graph.nodes.keys()):
            kept: List[NodeRecord] = []
            for record in self.graph.nodes[node_id]:
                if record.timeline_id == timeline_id and record.server_mode == ServerMode.LAB:
                    removed_nodes += 1
                    continue
                kept.append(record)
            if kept:
                self.graph.nodes[node_id] = kept
            else:
                del self.graph.nodes[node_id]

        original_edges = len(self.graph.edges)
        self.graph.edges = [
            edge
            for edge in self.graph.edges
            if not (edge.timeline_id == timeline_id and edge.server_mode == ServerMode.LAB)
        ]
        removed_edges = original_edges - len(self.graph.edges)
        self.graph.audit_log.append(f"reset_lab:{timeline_id}:nodes={removed_nodes}:edges={removed_edges}")
        return ResetReport(removed_lab_nodes=removed_nodes, removed_lab_edges=removed_edges)
