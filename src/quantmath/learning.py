"""Small, framework-free learning primitives for the teaching library."""

import math

import numpy as np


def _as_finite_array(value: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def scaled_dot_product_attention(
    queries: np.ndarray,
    keys: np.ndarray,
    values: np.ndarray,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """Compute row-wise scaled dot-product attention for 2-D arrays."""
    queries = _as_finite_array(queries, "queries")
    keys = _as_finite_array(keys, "keys")
    values = _as_finite_array(values, "values")
    if queries.ndim != 2 or keys.ndim != 2 or values.ndim != 2:
        raise ValueError("queries, keys, and values must be two-dimensional")
    if queries.shape[1] != keys.shape[1] or keys.shape[0] != values.shape[0]:
        raise ValueError("attention dimensions do not match")
    scores = queries @ keys.T / math.sqrt(queries.shape[1])
    if mask is not None:
        mask = np.asarray(mask, dtype=bool)
        if mask.shape != scores.shape:
            raise ValueError("mask must match the attention score shape")
        if np.any(~mask.any(axis=1)):
            raise ValueError("each query must be allowed to attend to at least one key")
        scores = np.where(mask, scores, -np.inf)
    shifted = scores - np.max(scores, axis=1, keepdims=True)
    weights = np.exp(shifted)
    weights /= weights.sum(axis=1, keepdims=True)
    return weights @ values


def adam_step(
    parameters: np.ndarray,
    gradients: np.ndarray,
    first_moment: np.ndarray,
    second_moment: np.ndarray,
    step: int,
    learning_rate: float = 1e-3,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform one bias-corrected Adam update."""
    parameters = _as_finite_array(parameters, "parameters")
    gradients = _as_finite_array(gradients, "gradients")
    first_moment = _as_finite_array(first_moment, "first_moment")
    second_moment = _as_finite_array(second_moment, "second_moment")
    if not (parameters.shape == gradients.shape == first_moment.shape == second_moment.shape):
        raise ValueError("Adam arrays must have the same shape")
    if step <= 0 or learning_rate <= 0 or epsilon <= 0 or not 0 <= beta1 < 1 or not 0 <= beta2 < 1:
        raise ValueError("invalid Adam hyperparameters")
    first = beta1 * first_moment + (1.0 - beta1) * gradients
    second = beta2 * second_moment + (1.0 - beta2) * gradients**2
    first_hat = first / (1.0 - beta1**step)
    second_hat = second / (1.0 - beta2**step)
    updated = parameters - learning_rate * first_hat / (np.sqrt(second_hat) + epsilon)
    return updated, first, second


def diffusion_forward(x0: np.ndarray, noise: np.ndarray, alpha_bar: float) -> np.ndarray:
    """Sample q(x_t | x_0) for a scalar cumulative diffusion schedule."""
    x0 = _as_finite_array(x0, "x0")
    noise = _as_finite_array(noise, "noise")
    if x0.shape != noise.shape:
        raise ValueError("x0 and noise must have the same shape")
    if not math.isfinite(alpha_bar) or not 0 <= alpha_bar <= 1:
        raise ValueError("alpha_bar must lie in [0, 1]")
    return math.sqrt(alpha_bar) * x0 + math.sqrt(1.0 - alpha_bar) * noise
