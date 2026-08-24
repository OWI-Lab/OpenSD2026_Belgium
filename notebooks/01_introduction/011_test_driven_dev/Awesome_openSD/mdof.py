"""A linear multi-degree-of-freedom (MDOF) system.

The system is represented in state-space form and simulated with SciPy's
``lsim`` function. It is defined by mass, damping, and stiffness matrices and
supports initial conditions and external forces.

Run the tests with ``uv run pytest``.
"""

import numpy as np
from scipy.linalg import eigh
from scipy.signal import lsim


class MDOFSystem:
    """Linear MDOF system: M ẍ + C ẋ + K x = f(t)."""

    def __init__(self, mass: np.ndarray, damping: np.ndarray, stiffness: np.ndarray):
        self.M = np.asarray(mass, dtype=float)
        self.C = np.asarray(damping, dtype=float)
        self.K = np.asarray(stiffness, dtype=float)

        if self.M.ndim != 2 or self.M.shape[0] != self.M.shape[1]:
            raise ValueError("Mass matrix must be square.")
        if self.C.shape != self.M.shape or self.K.shape != self.M.shape:
            raise ValueError("M, C, and K must have the same shape.")
        if np.min(np.linalg.eigvalsh(self.M)) <= 0:
            raise ValueError("Mass matrix must be positive definite.")
        if np.min(np.linalg.eigvalsh(self.C)) < -1e-6:
            raise ValueError("Damping matrix must be positive semidefinite.")
        if np.min(np.linalg.eigvalsh(self.K)) < -1e-6:
            raise ValueError("Stiffness matrix must be positive semidefinite.")

        self.n_dof = self.M.shape[0]

    def natural_frequencies_hz(self):
        eigenvalues = eigh(self.K, self.M, eigvals_only=True)
        if np.any(eigenvalues < 0):
            raise ValueError(
                "Negative eigenvalues encountered; check stiffness and mass matrices."
            )
        return np.sqrt(eigenvalues) / (2.0 * np.pi)

    def simulate(self, time, x0=None, v0=None, force=None):
        time = np.asarray(time, dtype=float)

        if time.ndim != 1 or time.size < 2:
            raise ValueError("time must be a one-dimensional array.")

        time_steps = np.diff(time)
        if np.any(time_steps <= 0):
            raise ValueError("time must be strictly increasing.")
        if not np.allclose(time_steps, time_steps[0]):
            raise ValueError("time must be equally spaced for lsim.")

        x0 = np.zeros(self.n_dof) if x0 is None else np.asarray(x0, dtype=float)
        v0 = np.zeros(self.n_dof) if v0 is None else np.asarray(v0, dtype=float)
        force = (
            np.zeros((time.size, self.n_dof))
            if force is None
            else np.asarray(force, dtype=float)
        )

        if x0.shape != (self.n_dof,) or v0.shape != (self.n_dof,):
            raise ValueError("x0 and v0 must contain one value per DOF.")
        if force.shape != (time.size, self.n_dof):
            raise ValueError("force must contain one value per DOF at each time step.")

        zeros = np.zeros((self.n_dof, self.n_dof))
        identity = np.eye(self.n_dof)
        state_matrix = np.block(
            [
                [zeros, identity],
                [
                    -np.linalg.solve(self.M, self.K),
                    -np.linalg.solve(self.M, self.C),
                ],
            ]
        )
        input_matrix = np.vstack((zeros, np.linalg.solve(self.M, identity)))

        _, _, state = lsim(
            (
                state_matrix,
                input_matrix,
                np.eye(2 * self.n_dof),
                np.zeros((2 * self.n_dof, self.n_dof)),
            ),
            U=force,
            T=time - time[0],
            X0=np.concatenate((x0, v0)),
        )

        return state[:, : self.n_dof], state[:, self.n_dof :]
