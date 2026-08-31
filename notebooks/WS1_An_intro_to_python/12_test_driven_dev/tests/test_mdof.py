"""Tests for MDOFSystem using a fixture for the shared undamped setup.
Here we used fixture to prepare an environment for the test function.
Read more about fixture in the pytest [doc](https://docs.pytest.org/en/stable/explanation/fixtures.html)"""

import numpy as np
import pytest

from Awesome_openSD.mdof import MDOFSystem


@pytest.fixture
def undamped_system():
    """Return a fresh undamped two-DOF system for each requesting test."""
    # Reference for the expected values:
    # https://valdivia.staff.jade-hs.de/federmasse_en.html
    # Example: two masses with one fixed end.
    mass = np.eye(2)
    damping = np.zeros((2, 2))
    stiffness = 1e3 * np.array(
        [
            [2.0, -1.0],
            [-1.0, 2.0],
        ]
    )
    return MDOFSystem(mass=mass, damping=damping, stiffness=stiffness)


def test_mdof_natural_frequencies(undamped_system):
    expected_frequencies = np.sqrt([1000.0, 3000.0]) / (2.0 * np.pi)
    computed_frequencies = undamped_system.natural_frequencies_hz()
    assert np.allclose(computed_frequencies, expected_frequencies, rtol=1e-6)


def test_simulation_with_linearity(undamped_system):
    # The response to two forces applied separately and then added should equal
    # the response to the combined force.
    time = np.linspace(0, 20, 2_001)
    force1 = np.column_stack((np.sin(2 * time), np.zeros_like(time)))
    force2 = np.column_stack((np.zeros_like(time), np.cos(3 * time)))

    displacement1, _ = undamped_system.simulate(time, force=force1)
    displacement2, _ = undamped_system.simulate(time, force=force2)
    combined_displacement, _ = undamped_system.simulate(
        time,
        force=force1 + force2,
    )

    assert np.allclose(
        combined_displacement,
        displacement1 + displacement2,
        rtol=1e-6,
    )


def test_decay_of_energy_in_damped_system():
    system = MDOFSystem(
        mass=np.eye(2),
        damping=0.05 * np.eye(2),
        stiffness=np.array(
            [
                [2.0, -1.0],
                [-1.0, 2.0],
            ]
        ),
    )

    time = np.linspace(0.0, 20.0, 2_001)
    displacement, velocity = system.simulate(
        time,
        x0=np.array([1.0, 0.0]),
    )

    kinetic_energy = 0.5 * np.sum(
        (velocity @ system.M) * velocity,
        axis=1,
    )
    potential_energy = 0.5 * np.sum(
        (displacement @ system.K) * displacement,
        axis=1,
    )
    total_energy = kinetic_energy + potential_energy
    assert np.all(np.diff(total_energy) < 0)
