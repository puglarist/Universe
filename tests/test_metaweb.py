import unittest

from metaweb import (
    QueryScope,
    ResetServerIntegrator,
    ServerMode,
    StructuredKnowledgeGraph,
    TimelineAwareQueryLayer,
    get_device_profile,
)


class MetaWebTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = StructuredKnowledgeGraph()
        self.graph.registry.register_node_schema("court_case", {"title": str, "status": str})
        self.graph.access.register_mod("mod.slyfox", "slyfox")

    def test_codex_901_index_10k_deterministically(self):
        for i in range(10_000):
            self.graph.upsert_node(
                actor_id="mod.slyfox",
                role="mod",
                node_id=f"entity-{i}",
                node_type="entity",
                namespace="slyfox",
                data={"name": f"E-{i}"},
                timeline_id="t0",
                branch_id="main",
                server_mode=ServerMode.LAB,
                tick=i,
            )
        self.assertEqual(len(list(self.graph.iter_nodes())), 10_000)

        query = TimelineAwareQueryLayer(self.graph)
        results = query.search(QueryScope(timeline_id="t0", branch_id="main", tick_start=30, tick_end=35))
        self.assertEqual([n.tick for n in results], [30, 31, 32, 33, 34, 35])

    def test_codex_902_timeline_aware_fork_differences(self):
        for branch in ("fork-a", "fork-b"):
            self.graph.upsert_node(
                actor_id="mod.slyfox",
                role="mod",
                node_id=f"case-{branch}",
                node_type="court_case",
                namespace="slyfox",
                data={"title": "v. Simulation", "status": branch},
                timeline_id="t1",
                branch_id=branch,
                server_mode=ServerMode.LAB,
                tick=5100,
            )
        q = TimelineAwareQueryLayer(self.graph)
        a = q.search(QueryScope(timeline_id="t1", branch_id="fork-a"))
        b = q.search(QueryScope(timeline_id="t1", branch_id="fork-b"))
        self.assertNotEqual([n.node_id for n in a], [n.node_id for n in b])

    def test_codex_904_reset_server(self):
        self.graph.upsert_node(
            actor_id="admin.root",
            role="admin",
            node_id="canon-law",
            node_type="law",
            namespace="core",
            data={"title": "Canonical"},
            timeline_id="t2",
            branch_id="main",
            server_mode=ServerMode.CANONICAL,
            tick=1,
        )
        self.graph.upsert_node(
            actor_id="mod.slyfox",
            role="mod",
            node_id="lab-law",
            node_type="law",
            namespace="slyfox",
            data={"title": "Lab"},
            timeline_id="t2",
            branch_id="exp",
            server_mode=ServerMode.LAB,
            tick=2,
        )

        report = ResetServerIntegrator(self.graph).reset_lab_server("t2")
        self.assertGreaterEqual(report.removed_lab_nodes, 1)
        self.assertIsNotNone(self.graph.latest_node("canon-law"))
        self.assertIsNone(self.graph.latest_node("lab-law"))

    def test_codex_905_canonical_protection(self):
        with self.assertRaises(PermissionError):
            self.graph.upsert_node(
                actor_id="mod.slyfox",
                role="mod",
                node_id="canon-overwrite",
                node_type="law",
                namespace="slyfox",
                data={"title": "Bad"},
                timeline_id="t3",
                branch_id="main",
                server_mode=ServerMode.CANONICAL,
                tick=100,
            )

    def test_codex_903_navigator_admin_profile(self):
        profile = get_device_profile("slyfox_admin_overlay", admin_mode=True)
        self.assertEqual(profile["app"], "MetaWeb Navigator")
        self.assertTrue(profile["features"].raw_query_console)


if __name__ == "__main__":
    unittest.main()
