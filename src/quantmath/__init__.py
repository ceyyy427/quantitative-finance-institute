"""Reusable code for the Quantitative Finance Institute."""

__version__ = "0.5.0"

from .genomics import benjamini_hochberg, pca_svd, standardize_matrix
from .hedging import DeltaHedgeResult, simulate_delta_hedge
from .learning import adam_step, diffusion_forward, scaled_dot_product_attention
from .operations import (
    dijkstra_shortest_path,
    economic_order_quantity,
    newsvendor_quantity,
    value_iteration,
)
from .quantum import apply_single_qubit_gate, hadamard_state

__all__ = [
    "DeltaHedgeResult",
    "__version__",
    "adam_step",
    "apply_single_qubit_gate",
    "benjamini_hochberg",
    "diffusion_forward",
    "dijkstra_shortest_path",
    "economic_order_quantity",
    "hadamard_state",
    "newsvendor_quantity",
    "pca_svd",
    "scaled_dot_product_attention",
    "simulate_delta_hedge",
    "standardize_matrix",
    "value_iteration",
]
