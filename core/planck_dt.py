from __future__ import annotations

from datetime import datetime, timezone
import math
import random


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_summary(steps: int = 40, twins: int = 3, policy: str = "rule") -> dict:
    rng = random.Random(42)
    route_counts = {"CLASSICAL": 0, "QUANTUM": 0, "FALLBACK_CLASSICAL": 0}
    recent_records = []

    for step in range(1, steps + 1):
        twin_id = f"infra:asset:{(step % max(1, twins)) + 1:03d}"
        signal = abs(math.sin(step / 5.0)) + 0.15 * rng.random()

        if policy == "bandit" and signal > 0.75:
            route = "QUANTUM"
        elif signal > 0.9:
            route = "FALLBACK_CLASSICAL"
        else:
            route = "CLASSICAL"

        route_counts[route] += 1

        recent_records.append(
            {
                "step_id": step,
                "timestamp": utc_now_iso(),
                "twin_id": twin_id,
                "route": route,
                "exec_ms": round(10 + 90 * rng.random(), 2),
                "objective_value": round(-0.5 - 2.0 * signal, 4),
                "confidence": round(max(0.2, 0.95 - 0.4 * signal), 4),
            }
        )

    mean_exec_ms = round(
        sum(r["exec_ms"] for r in recent_records) / len(recent_records), 3
    ) if recent_records else 0.0

    mean_objective = round(
        sum(r["objective_value"] for r in recent_records) / len(recent_records), 4
    ) if recent_records else 0.0

    return {
        "system": "Planck DT",
        "steps": steps,
        "twins": twins,
        "policy": policy,
        "records": len(recent_records),
        "mean_objective": mean_objective,
        "mean_exec_ms": mean_exec_ms,
        "latency_breach_rate": 0.0,
        "route_counts": route_counts,
        "recent_records": recent_records[-10:],
    }
