"""Resource-allocation strategies for the cloud allocation simulator."""
from typing import Dict, List, Any

Request = Dict[str, Any]


def allocate_fcfs(requests: List[Request], total_cpu: int, total_ram: int) -> dict:
    """Allocate resources in request-arrival order if both CPU and RAM fit."""
    available_cpu, available_ram = total_cpu, total_ram
    accepted, rejected = [], []

    for request in requests:
        if request["cpu"] <= available_cpu and request["ram"] <= available_ram:
            accepted.append({**request, "status": "Accepted"})
            available_cpu -= request["cpu"]
            available_ram -= request["ram"]
        else:
            rejected.append({**request, "status": "Rejected"})

    return _result(accepted, rejected, total_cpu, total_ram)


def allocate_priority(requests: List[Request], total_cpu: int, total_ram: int) -> dict:
    """Allocate higher-priority requests first; preserve arrival order for ties."""
    ordered = sorted(
        enumerate(requests),
        key=lambda item: (-int(item[1]["priority"]), item[0])
    )
    ordered_requests = [request for _, request in ordered]
    return allocate_fcfs(ordered_requests, total_cpu, total_ram)


def _result(accepted: list, rejected: list, total_cpu: int, total_ram: int) -> dict:
    used_cpu = sum(r["cpu"] for r in accepted)
    used_ram = sum(r["ram"] for r in accepted)
    return {
        "accepted": accepted,
        "rejected": rejected,
        "used_cpu": used_cpu,
        "used_ram": used_ram,
        "available_cpu": total_cpu - used_cpu,
        "available_ram": total_ram - used_ram,
        "total_cpu": total_cpu,
        "total_ram": total_ram,
    }
