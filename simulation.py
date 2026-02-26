"""Simple universe simulation model.

The simulation tracks stars, planets, and colonies through a number of steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List


@dataclass
class Planet:
    """A planet with finite resources and population."""

    name: str
    resources: float
    population: float

    def advance(self, rng: Random) -> None:
        """Advance one tick of growth/consumption."""
        growth = rng.uniform(0.01, 0.07)
        extraction = rng.uniform(0.02, 0.05)

        self.population *= 1 + growth
        self.resources -= self.population * extraction
        self.resources = max(self.resources, 0.0)


@dataclass
class StarSystem:
    """Collection of planets around a single star."""

    name: str
    planets: List[Planet]

    def advance(self, rng: Random) -> None:
        for planet in self.planets:
            planet.advance(rng)

    @property
    def total_population(self) -> float:
        return sum(p.population for p in self.planets)

    @property
    def total_resources(self) -> float:
        return sum(p.resources for p in self.planets)


class UniverseSimulation:
    """Main controller for the Universe simulation."""

    def __init__(self, seed: int = 42) -> None:
        self.rng = Random(seed)
        self.time = 0
        self.systems = self._bootstrap()

    def _bootstrap(self) -> List[StarSystem]:
        return [
            StarSystem(
                name="Helios",
                planets=[
                    Planet("Astra", resources=1000.0, population=110.0),
                    Planet("Boreal", resources=750.0, population=80.0),
                ],
            ),
            StarSystem(
                name="Orion",
                planets=[
                    Planet("Cinder", resources=1500.0, population=140.0),
                    Planet("Dawn", resources=620.0, population=60.0),
                ],
            ),
        ]

    def step(self, n: int = 1) -> None:
        for _ in range(n):
            for system in self.systems:
                system.advance(self.rng)
            self.time += 1

    def summary(self) -> str:
        lines = [f"Universe step: {self.time}"]
        for system in self.systems:
            lines.append(
                f"- {system.name}: population={system.total_population:.1f}, "
                f"resources={system.total_resources:.1f}"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    sim = UniverseSimulation()
    sim.step(10)
    print(sim.summary())
