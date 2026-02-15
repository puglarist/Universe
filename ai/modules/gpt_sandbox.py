"""Minimal GPT sandbox module for Patch 0 foundation testing.

Usage:
    export OPENAI_API_KEY=...
    python ai/modules/gpt_sandbox.py --mode npc-dialogue --prompt "Greet the player"
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass


@dataclass
class SandboxRequest:
    mode: str
    prompt: str


def build_system_prompt(mode: str) -> str:
    presets = {
        "npc-dialogue": "Generate concise in-game NPC dialogue.",
        "object-seed": "Generate a short procedural object concept.",
        "environment-layout": "Generate a high-level environment layout concept.",
    }
    return presets.get(mode, "Generate concise structured game content.")


def run_sandbox(req: SandboxRequest) -> str:
    """Return a simulated response until live API integration is enabled."""
    if not os.getenv("OPENAI_API_KEY"):
        return (
            "[sandbox:offline] OPENAI_API_KEY not set. "
            f"Mode={req.mode}; Prompt={req.prompt}"
        )

    # Placeholder behavior while wiring SDK/network policies.
    return (
        "[sandbox:online-placeholder] API key detected. "
        "Replace this branch with SDK-backed inference call. "
        f"SystemPrompt={build_system_prompt(req.mode)}; UserPrompt={req.prompt}"
    )


def parse_args() -> SandboxRequest:
    parser = argparse.ArgumentParser(description="Universe GPT sandbox")
    parser.add_argument(
        "--mode",
        default="npc-dialogue",
        choices=["npc-dialogue", "object-seed", "environment-layout"],
        help="Type of generation to test.",
    )
    parser.add_argument("--prompt", required=True, help="Prompt payload to test.")
    args = parser.parse_args()
    return SandboxRequest(mode=args.mode, prompt=args.prompt)


if __name__ == "__main__":
    request = parse_args()
    print(run_sandbox(request))
