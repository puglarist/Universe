#!/usr/bin/env python3
"""
Inner Bridge: a terminal rehearsal tool for meditative and imaginative control loops.

This script does not claim supernatural effects. It helps build repeatable mental patterns
using breath pacing, intention repetition, and symbolic gestures.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


DEFAULT_PLAN = {
    "name": "Lucid Interface Seed",
    "intention": "I calmly notice symbols and choose my next action with clarity.",
    "breath": {"inhale": 4, "hold": 2, "exhale": 6, "cycles": 4},
    "visual_symbols": ["ORB", "DOOR", "TERMINAL", "STAR"],
    "gesture_map": {
        "focus": "f",
        "open-terminal": "t",
        "stabilize-scene": "s",
        "wake-softly": "w",
    },
    "repetitions": 3,
    "encoding_notes": "Replay each symbol in order while imagining one tiny UI action.",
}


@dataclass
class SessionPlan:
    name: str
    intention: str
    breath: Dict[str, int]
    visual_symbols: List[str]
    gesture_map: Dict[str, str]
    repetitions: int
    encoding_notes: str

    @classmethod
    def from_dict(cls, data: Dict) -> "SessionPlan":
        return cls(
            name=data["name"],
            intention=data["intention"],
            breath=data["breath"],
            visual_symbols=list(data["visual_symbols"]),
            gesture_map=dict(data["gesture_map"]),
            repetitions=int(data["repetitions"]),
            encoding_notes=data["encoding_notes"],
        )


def load_plan(path: Path) -> SessionPlan:
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_PLAN, indent=2))
        print(f"Created default plan at {path}")
    data = json.loads(path.read_text())
    return SessionPlan.from_dict(data)


def save_plan(path: Path, plan: SessionPlan) -> None:
    path.write_text(json.dumps(asdict(plan), indent=2))


def countdown(label: str, seconds: int, speed: float) -> None:
    print(f"  {label} ({seconds}s)")
    for remaining in range(seconds, 0, -1):
        print(f"    {remaining}", end="\r", flush=True)
        time.sleep(max(0.05, 1.0 / speed))
    print(" " * 20, end="\r")


def run_breath_cycle(plan: SessionPlan, speed: float) -> None:
    b = plan.breath
    cycles = b.get("cycles", 4)
    print(f"\nBreath cycles: {cycles}")
    for idx in range(1, cycles + 1):
        print(f"Cycle {idx}/{cycles}")
        countdown("Inhale", b.get("inhale", 4), speed)
        countdown("Hold", b.get("hold", 2), speed)
        countdown("Exhale", b.get("exhale", 6), speed)


def run_encoding_round(plan: SessionPlan, round_number: int, speed: float) -> None:
    print(f"\n--- Encoding Round {round_number}/{plan.repetitions} ---")
    print(f"Intention: {plan.intention}")
    time.sleep(max(0.1, 0.7 / speed))

    print("Visual sequence:")
    for symbol in plan.visual_symbols:
        print(f"  [{symbol}] -> imagine one small interface gesture")
        time.sleep(max(0.1, 0.9 / speed))

    print("Gesture bindings (symbolic rehearsal):")
    for action, key in plan.gesture_map.items():
        print(f"  {key}: {action}")
        time.sleep(max(0.05, 0.45 / speed))

    print(f"Note: {plan.encoding_notes}")


def run_session(plan: SessionPlan, speed: float) -> None:
    print(f"\n=== {plan.name} ===")
    print("This is a mental rehearsal protocol for focus and imagination training.")
    run_breath_cycle(plan, speed)

    for i in range(1, plan.repetitions + 1):
        run_encoding_round(plan, i, speed)

    print("\nSession complete.")
    print("Close your eyes and replay the same sequence slowly from memory.")


def interactive_edit(plan: SessionPlan) -> SessionPlan:
    print("\nInteractive quick-edit (press Enter to keep current value)")
    name = input(f"Plan name [{plan.name}]: ").strip() or plan.name
    intention = input(f"Intention [{plan.intention}]: ").strip() or plan.intention
    repetitions_raw = input(f"Repetitions [{plan.repetitions}]: ").strip()
    repetitions = int(repetitions_raw) if repetitions_raw else plan.repetitions

    symbols_raw = input(
        "Visual symbols comma-separated "
        f"[{', '.join(plan.visual_symbols)}]: "
    ).strip()
    symbols = [s.strip().upper() for s in symbols_raw.split(",") if s.strip()] if symbols_raw else plan.visual_symbols

    print("Current gesture map:")
    for action, key in plan.gesture_map.items():
        new_key = input(f"  Key for '{action}' [{key}]: ").strip()
        if new_key:
            plan.gesture_map[action] = new_key

    plan.name = name
    plan.intention = intention
    plan.repetitions = repetitions
    plan.visual_symbols = symbols
    return plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inner Bridge rehearsal CLI")
    parser.add_argument(
        "--plan",
        type=Path,
        default=Path("bridge_plan.json"),
        help="Path to plan JSON",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=2.0,
        help="Playback speed multiplier (higher = faster)",
    )
    parser.add_argument(
        "--edit",
        action="store_true",
        help="Interactively edit the plan before running",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan = load_plan(args.plan)

    if args.edit:
        plan = interactive_edit(plan)
        save_plan(args.plan, plan)
        print(f"Saved updated plan to {args.plan}")

    run_session(plan, args.speed)


if __name__ == "__main__":
    main()
