"""Metrics used to compare allocation strategies."""


def calculate_metrics(result: dict, total_requests: int) -> dict:
    total_cpu = result["total_cpu"]
    total_ram = result["total_ram"]
    accepted_count = len(result["accepted"])
    return {
        "CPU utilization (%)": round(100 * result["used_cpu"] / total_cpu, 2) if total_cpu else 0,
        "RAM utilization (%)": round(100 * result["used_ram"] / total_ram, 2) if total_ram else 0,
        "Accepted requests": accepted_count,
        "Rejected requests": len(result["rejected"]),
        "Acceptance rate (%)": round(100 * accepted_count / total_requests, 2) if total_requests else 0,
    }
