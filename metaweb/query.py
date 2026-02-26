from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .graph_engine import StructuredKnowledgeGraph
from .schema import NodeRecord, ServerMode


@dataclass
class QueryScope:
    timeline_id: Optional[str] = None
    branch_id: Optional[str] = None
    server_mode: Optional[ServerMode] = None
    tick_start: Optional[int] = None
    tick_end: Optional[int] = None
    node_type: Optional[str] = None


class TimelineAwareQueryLayer:
    def __init__(self, graph: StructuredKnowledgeGraph) -> None:
        self.graph = graph

    def search(self, scope: QueryScope) -> List[NodeRecord]:
        results: List[NodeRecord] = []
        for node in self.graph.iter_nodes():
            if scope.timeline_id and node.timeline_id != scope.timeline_id:
                continue
            if scope.branch_id and node.branch_id != scope.branch_id:
                continue
            if scope.server_mode and node.server_mode != scope.server_mode:
                continue
            if scope.node_type and node.node_type != scope.node_type:
                continue
            if scope.tick_start is not None and node.tick < scope.tick_start:
                continue
            if scope.tick_end is not None and node.tick > scope.tick_end:
                continue
            results.append(node)
        return sorted(results, key=lambda n: (n.tick, n.node_id, n.version))
