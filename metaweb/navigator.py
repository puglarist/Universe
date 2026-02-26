from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NavigatorFeatureSet:
    structured_query_builder: bool = True
    visual_graph_explorer: bool = True
    timeline_slider: bool = True
    fork_comparison_panel: bool = True
    replay_viewer: bool = True
    diff_visualizer: bool = True
    raw_query_console: bool = False
    causal_chain_explorer: bool = False
    integrity_tracing: bool = False


def get_device_profile(device_type: str, admin_mode: bool = False) -> Dict[str, object]:
    supported = {"laptop", "phone", "slyfox_admin_overlay"}
    if device_type not in supported:
        raise ValueError("Unsupported device for MetaWeb Navigator")

    features = NavigatorFeatureSet(
        raw_query_console=admin_mode,
        causal_chain_explorer=admin_mode,
        integrity_tracing=admin_mode,
    )
    return {
        "device_type": device_type,
        "app": "MetaWeb Navigator",
        "admin_mode": admin_mode,
        "features": features,
    }


def build_mod_builder_requirements() -> List[str]:
    return [
        "register_schema",
        "declare_namespace",
        "define_data_permissions",
        "pass_integrity_validation",
    ]
