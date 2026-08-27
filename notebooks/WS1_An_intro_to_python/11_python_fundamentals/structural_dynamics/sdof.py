import numpy as np


class SDOFSystem:
    """
    Represent a single-degree-of-freedom (SDOF) structural system.

    Parameters
    ----------
    mass : float
        Mass of the system in kg.
    stiffness : float
        Stiffness of the system in N/m.
    damping : float
        Damping coefficient in N·s/m.
    """

    def __init__(self, mass, stiffness, damping):
        self.mass = mass
        self.stiffness = stiffness
        self.damping = damping

    def natural_frequency(self):
        """
        Calculate the undamped natural frequency.

        Returns
        -------
        float
            Natural frequency in Hz.
        """
        return np.sqrt(self.stiffness / self.mass) / (2 * np.pi)

    def critical_damping(self):
        """
        Calculate the critical damping coefficient.

        Returns
        -------
        float
            Critical damping coefficient in N·s/m.
        """
        return 2 * np.sqrt(self.mass * self.stiffness)

    def damping_ratio(self):
        """
        Calculate the damping ratio.

        Returns
        -------
        float
            Damping ratio.
        """
        return self.damping / self.critical_damping()