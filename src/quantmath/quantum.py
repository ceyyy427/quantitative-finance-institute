"""Minimal state-vector operations for the quantum-computing primer."""

import numpy as np


def apply_single_qubit_gate(gate: np.ndarray, state: np.ndarray) -> np.ndarray:
    """Apply a 2x2 complex gate to a normalized one-qubit state."""
    gate = np.asarray(gate, dtype=complex)
    state = np.asarray(state, dtype=complex)
    if gate.shape != (2, 2) or state.shape != (2,):
        raise ValueError("gate must be 2x2 and state must have length two")
    if not np.all(np.isfinite(gate.real)) or not np.all(np.isfinite(gate.imag)):
        raise ValueError("gate must be finite")
    if not np.allclose(gate.conj().T @ gate, np.eye(2), atol=1e-10):
        raise ValueError("gate must be unitary")
    norm = np.linalg.norm(state)
    if not np.isclose(norm, 1.0):
        raise ValueError("state must be normalized")
    return gate @ state


def hadamard_state() -> np.ndarray:
    """Return H|0> = (|0>+|1>)/sqrt(2)."""
    return np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
