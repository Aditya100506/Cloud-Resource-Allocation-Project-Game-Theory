"""A simple normal-form game for two cloud tenants competing for priority."""
from itertools import product


def build_payoff_matrix():
    """
    Rows are Tenant A's actions; columns are Tenant B's actions.
    Actions: Low Bid, High Bid.
    Payoffs are illustrative net utility points, not market prices.
    """
    actions = ["Low Bid", "High Bid"]
    payoffs = {
        ("Low Bid", "Low Bid"): (5, 5),
        ("Low Bid", "High Bid"): (2, 7),
        ("High Bid", "Low Bid"): (7, 2),
        ("High Bid", "High Bid"): (3, 3),
    }
    return actions, payoffs


def pure_nash_equilibria():
    actions, payoffs = build_payoff_matrix()
    equilibria = []
    for a, b in product(actions, repeat=2):
        a_payoff, b_payoff = payoffs[(a, b)]
        a_best_response = a_payoff >= max(payoffs[(alt_a, b)][0] for alt_a in actions)
        b_best_response = b_payoff >= max(payoffs[(a, alt_b)][1] for alt_b in actions)
        if a_best_response and b_best_response:
            equilibria.append({"tenant_a": a, "tenant_b": b, "payoffs": payoffs[(a, b)]})
    return equilibria
