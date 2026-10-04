"""Small high-dimensional statistics primitives for the biomedical chapters."""

import numpy as np


def standardize_matrix(matrix: np.ndarray) -> np.ndarray:
    """Center and scale columns with sample standard deviation."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or not np.all(np.isfinite(matrix)):
        raise ValueError("matrix must be a finite 2-D array with at least two rows")
    mean = matrix.mean(axis=0)
    scale = matrix.std(axis=0, ddof=1)
    if np.any(scale == 0):
        raise ValueError("constant columns cannot be standardized")
    return (matrix - mean) / scale


def pca_svd(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return right singular vectors and explained variance ratios."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or not np.all(np.isfinite(matrix)):
        raise ValueError("matrix must be a finite 2-D array with at least two rows")
    centered = matrix - matrix.mean(axis=0)
    _, singular_values, right_singular_vectors = np.linalg.svd(centered, full_matrices=False)
    variance = singular_values**2
    explained = variance / variance.sum() if variance.sum() > 0 else np.zeros_like(variance)
    return right_singular_vectors.T, explained


def benjamini_hochberg(p_values: np.ndarray, q: float = 0.05) -> np.ndarray:
    """Return hypotheses rejected by the Benjamini-Hochberg step-up rule."""
    p_values = np.asarray(p_values, dtype=float)
    if p_values.ndim != 1 or p_values.size == 0 or not np.all(np.isfinite(p_values)):
        raise ValueError("p_values must be a non-empty finite vector")
    if np.any((p_values < 0) | (p_values > 1)) or not 0 < q < 1:
        raise ValueError("p_values must lie in [0, 1] and q must lie in (0, 1)")
    order = np.argsort(p_values)
    sorted_values = p_values[order]
    thresholds = q * np.arange(1, p_values.size + 1) / p_values.size
    eligible = np.flatnonzero(sorted_values <= thresholds)
    rejected = np.zeros(p_values.size, dtype=bool)
    if eligible.size:
        rejected[order[: eligible[-1] + 1]] = True
    return rejected
