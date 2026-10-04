"""Transparent operations-research algorithms used in applied chapters."""

import heapq
import math

import numpy as np


def value_iteration(
    transitions: dict[int, dict[int, list[tuple[int, float, float]]]],
    gamma: float = 0.9,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Solve a finite discounted MDP by Bellman iteration."""
    if not 0 <= gamma < 1 or tolerance <= 0 or max_iterations <= 0:
        raise ValueError("invalid value-iteration hyperparameters")
    n_states = len(transitions)
    if set(transitions) != set(range(n_states)):
        raise ValueError("states must be consecutive integers starting at zero")
    values = np.zeros(n_states, dtype=float)
    policy = np.zeros(n_states, dtype=int)
    for iteration in range(1, max_iterations + 1):
        updated = np.empty_like(values)
        for state, actions in transitions.items():
            if not actions:
                raise ValueError(f"state {state} has no actions")
            action_values = []
            for outcomes in actions.values():
                probability_sum = sum(probability for _, probability, _ in outcomes)
                if not np.isclose(probability_sum, 1.0) or any(probability < 0 for _, probability, _ in outcomes):
                    raise ValueError("transition probabilities must be non-negative and sum to one")
                action_values.append(
                    sum(probability * (reward + gamma * values[next_state])
                        for next_state, probability, reward in outcomes)
                )
            index = int(np.argmax(action_values))
            policy[state] = list(actions)[index]
            updated[state] = action_values[index]
        error = float(np.max(np.abs(updated - values)))
        values = updated
        if error < tolerance:
            return values, policy, iteration
    raise RuntimeError("value iteration did not converge")


def economic_order_quantity(demand_rate: float, ordering_cost: float, holding_cost: float) -> float:
    """Return the EOQ sqrt(2DS/H) quantity."""
    if not all(math.isfinite(value) for value in (demand_rate, ordering_cost, holding_cost)):
        raise ValueError("EOQ inputs must be finite")
    if demand_rate <= 0 or ordering_cost <= 0 or holding_cost <= 0:
        raise ValueError("EOQ inputs must be positive")
    return math.sqrt(2.0 * demand_rate * ordering_cost / holding_cost)


def newsvendor_quantity(
    demand: np.ndarray, underage_cost: float, overage_cost: float
) -> float:
    """Return the empirical critical-fractile order quantity."""
    demand = np.asarray(demand, dtype=float)
    if demand.ndim != 1 or demand.size == 0 or not np.all(np.isfinite(demand)):
        raise ValueError("demand must be a non-empty finite vector")
    if np.any(demand < 0) or underage_cost <= 0 or overage_cost <= 0:
        raise ValueError("demand and costs must be valid")
    fractile = underage_cost / (underage_cost + overage_cost)
    return float(np.quantile(demand, fractile, method="lower"))


def newevendor_quantity(demand: np.ndarray, underage_cost: float, overage_cost: float) -> float:
    """Backward-compatible teaching alias for :func:`newsvendor_quantity`."""
    return newsvendor_quantity(demand, underage_cost, overage_cost)


def dijkstra_shortest_path(
    graph: dict[str, dict[str, float] | list[tuple[str, float]]], start: str, target: str
) -> tuple[float, list[str]]:
    """Return the shortest non-negative weighted path in a directed graph."""
    if start not in graph or target not in graph:
        raise ValueError("start and target must be graph nodes")
    adjacency: dict[str, dict[str, float]] = {}
    for node, edges in graph.items():
        if isinstance(edges, dict):
            adjacency[node] = {neighbor: float(weight) for neighbor, weight in edges.items()}
        else:
            adjacency[node] = {neighbor: float(weight) for neighbor, weight in edges}
    if any(weight < 0 for edges in adjacency.values() for weight in edges.values()):
        raise ValueError("Dijkstra requires non-negative edge weights")
    if any(neighbor not in graph for edges in adjacency.values() for neighbor in edges):
        raise ValueError("all edge endpoints must be graph nodes")
    distances = {node: math.inf for node in graph}
    previous: dict[str, str | None] = {node: None for node in graph}
    distances[start] = 0.0
    queue = [(0.0, start)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        if node == target:
            break
        for neighbor, weight in adjacency[node].items():
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    if math.isinf(distances[target]):
        raise ValueError("target is unreachable")
    path = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = previous[node]
    return distances[target], list(reversed(path))
