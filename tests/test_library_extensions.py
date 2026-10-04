import numpy as np
import pytest

from quantmath.genomics import benjamini_hochberg, pca_svd, standardize_matrix
from quantmath.learning import adam_step, diffusion_forward, scaled_dot_product_attention
from quantmath.operations import (
    dijkstra_shortest_path,
    economic_order_quantity,
    newevendor_quantity,
    value_iteration,
)
from quantmath.quantum import apply_single_qubit_gate, hadamard_state


def test_scaled_dot_product_attention_preserves_value_shape_and_rows_sum_to_one():
    queries = np.eye(2)
    result = scaled_dot_product_attention(queries, queries, queries)
    assert result.shape == (2, 2)
    assert np.all(np.isfinite(result))


def test_adam_step_moves_parameter_against_gradient():
    parameters = np.array([1.0, -1.0])
    first = np.zeros(2)
    second = np.zeros(2)
    updated, first, second = adam_step(parameters, np.array([1.0, -2.0]), first, second, 1)
    assert updated[0] < parameters[0]
    assert updated[1] > parameters[1]


def test_diffusion_forward_matches_closed_form_at_zero_noise():
    x0 = np.array([1.0, -2.0])
    assert np.allclose(diffusion_forward(x0, np.zeros(2), alpha_bar=0.81), 0.9 * x0)


def test_value_iteration_finds_highest_reward_action():
    transitions = {0: {0: [(0, 1.0, 1.0)], 1: [(0, 1.0, 2.0)]}}
    values, policy, _ = value_iteration(transitions, gamma=0.5)
    assert values[0] == pytest.approx(4.0)
    assert policy[0] == 1


def test_economic_order_quantity_is_positive():
    assert economic_order_quantity(100.0, 20.0, 5.0) == pytest.approx(28.284271)


def test_newsvendor_quantity_uses_quantile():
    demand = np.array([1.0, 2.0, 3.0, 4.0])
    assert newevendor_quantity(demand, underage_cost=3.0, overage_cost=1.0) == pytest.approx(3.0)


def test_dijkstra_returns_shortest_path_and_distance():
    graph = {"a": {"b": 2.0, "c": 5.0}, "b": {"c": 1.0}, "c": {}}
    distance, path = dijkstra_shortest_path(graph, "a", "c")
    assert distance == pytest.approx(3.0)
    assert path == ["a", "b", "c"]


def test_dijkstra_accepts_adjacency_lists_for_teaching_examples():
    graph = {"a": [("b", 2.0)], "b": [("c", 1.0)], "c": []}
    distance, path = dijkstra_shortest_path(graph, "a", "c")
    assert distance == pytest.approx(3.0)
    assert path == ["a", "b", "c"]


def test_benjamini_hochberg_returns_boolean_rejections():
    rejected = benjamini_hochberg(np.array([0.001, 0.01, 0.8, 0.9]), q=0.05)
    assert rejected.tolist() == [True, True, False, False]


def test_pca_svd_returns_orthonormal_components():
    matrix = np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]])
    components, explained = pca_svd(standardize_matrix(matrix))
    assert components.shape == (2, 2)
    assert np.allclose(components @ components.T, np.eye(2), atol=1e-10)
    assert explained[0] > explained[1]


def test_pca_svd_components_are_feature_by_component_for_rectangular_matrix():
    matrix = np.arange(20.0).reshape(5, 4)
    components, explained = pca_svd(matrix)
    assert components.shape == (4, 4)
    assert explained.shape == (4,)
    assert np.allclose(components.T @ components, np.eye(4), atol=1e-10)


def test_hadamard_state_creates_equal_superposition():
    state = hadamard_state()
    assert np.allclose(np.abs(state), np.array([1.0, 1.0]) / np.sqrt(2))
    gate = np.array([[1.0, 0.0], [0.0, -1.0]])
    assert np.allclose(apply_single_qubit_gate(gate, state), np.array([1.0, -1.0]) / np.sqrt(2))


def test_invalid_attention_dimensions_raise():
    with pytest.raises(ValueError):
        scaled_dot_product_attention(np.ones((2, 3)), np.ones((4, 2)), np.ones((4, 2)))


def test_attention_rejects_query_rows_with_no_visible_keys():
    with pytest.raises(ValueError):
        scaled_dot_product_attention(
            np.ones((1, 2)), np.ones((2, 2)), np.ones((2, 2)), mask=np.zeros((1, 2), dtype=bool)
        )


def test_quantum_gate_must_be_unitary():
    with pytest.raises(ValueError):
        apply_single_qubit_gate(np.ones((2, 2)), hadamard_state())
