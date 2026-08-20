import numpy as np
from Awesome_openSD.mdof import MDOFSystem
import matplotlib.pyplot as plt

def build_system():
    # external source to get the value : 
    # https://valdivia.staff.jade-hs.de/federmasse_en.html 
    # use examples :2m, fixed at one side 
    mass = np.eye(2)
    damping = np.zeros((2, 2))
    stiffness = np.array([
        [2.0, -1.0],
        [-1.0, 2.0],
    ])*1e3    
    return MDOFSystem(mass=mass, damping=damping, stiffness=stiffness)

def test_mdof_natural_frequencies():
    system = build_system()
    expected_frequencies = np.sqrt([1000.0, 3000.0]) / (2.0 * np.pi)
    computed_frequencies = system.natural_frequencies_hz()
    assert np.allclose(computed_frequencies, expected_frequencies, rtol=1e-6) 
    
    
def test_simulation_with_linearity():
    # two forces applied separately and then combined their response 
    # should be equal to the response of the combined force 
    system = build_system() 
    time = np.linspace(0,20, 2001) 
    force1 = np.column_stack((np.sin(2*time), np.zeros_like(time)))
    force2 = np.column_stack((np.zeros_like(time), np.cos(3*time)))
    force_combined = force1 + force2 
    
    desp1, vel1 = system.simulate(time, force=force1)
    desp2, vel2 = system.simulate(time, force=force2)
    desp_combined, vel_combined = system.simulate(time, force=force_combined)
    assert np.allclose(desp_combined, desp1 + desp2, rtol=1e-6)
    
def test_decay_of_energy_in_damped_system():
    system = MDOFSystem(
        mass=np.eye(2),
        damping=0.05 * np.eye(2),
        stiffness=np.array([
            [2.0, -1.0],
            [-1.0, 2.0],
        ]),
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
    decay = np.diff(total_energy) < 0
    assert np.all(decay)
