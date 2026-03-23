from core.planck_dt import run_summary


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def handler(request):
    params = getattr(request, "args", {}) or {}
    steps = max(5, min(200, _to_int(params.get("steps"), 40)))
    twins = max(1, min(10, _to_int(params.get("twins"), 3)))
    policy = params.get("policy", "rule")
    if policy not in {"rule", "bandit"}:
        policy = "rule"

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": run_summary(steps=steps, twins=twins, policy=policy),
    }
