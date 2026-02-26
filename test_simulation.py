from simulation import UniverseSimulation


def test_simulation_progresses_time_and_changes_state():
    sim = UniverseSimulation(seed=1)
    before = sim.summary()

    sim.step(5)

    assert sim.time == 5
    after = sim.summary()
    assert before != after
    assert "Universe step: 5" in after
