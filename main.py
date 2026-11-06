"""Run a command-line demo of the cloud resource allocation project."""
from algorithms import allocate_fcfs, allocate_priority
from metrics import calculate_metrics
from game_theory import pure_nash_equilibria

TOTAL_CPU = 8
TOTAL_RAM = 16

REQUESTS = [
    {"name": "App A", "cpu": 6, "ram": 8, "priority": 1},
    {"name": "App B", "cpu": 4, "ram": 8, "priority": 3},
    {"name": "App C", "cpu": 2, "ram": 8, "priority": 2},
]


def show_result(label, result):
    print(f"\n=== {label} ===")
    print("Accepted:", ", ".join(r["name"] for r in result["accepted"]) or "None")
    print("Rejected:", ", ".join(r["name"] for r in result["rejected"]) or "None")
    print(f"CPU used: {result['used_cpu']}/{TOTAL_CPU}")
    print(f"RAM used: {result['used_ram']}/{TOTAL_RAM}")
    for key, value in calculate_metrics(result, len(REQUESTS)).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    fcfs = allocate_fcfs(REQUESTS, TOTAL_CPU, TOTAL_RAM)
    priority = allocate_priority(REQUESTS, TOTAL_CPU, TOTAL_RAM)
    show_result("FCFS", fcfs)
    show_result("Priority-Based", priority)

    print("\n=== Strategic Game: Two Cloud Tenants ===")
    print("Pure-strategy Nash equilibrium(s):")
    for eq in pure_nash_equilibria():
        print(f"Tenant A: {eq['tenant_a']}, Tenant B: {eq['tenant_b']}, Payoffs: {eq['payoffs']}")
