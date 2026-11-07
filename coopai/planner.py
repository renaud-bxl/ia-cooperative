"""Greedy feasibility estimate for an explicitly uniform layer model.

No network discovery, model execution, GPU allocation or speed guarantee.
One trust group and one backend per plan; a partial plan is never admitted.
"""
from .policy import gb, quota_bytes, number

def positive_int(value, label):
    n = number(value, label)
    if n != int(n) or n == 0:
        raise ValueError(f"{label} must be a positive integer")
    return int(n)

def plan(config):
    model = config["model"]
    layers = positive_int(model["layers"], "layers")
    if model.get("uniform_layer_estimate") is not True:
        raise ValueError("Only explicit uniform-layer estimates are supported")
    weights = gb(model["weights_with_metadata_gb"])
    kv = gb(model["kv_total_gb"])
    per_layer = (weights + kv + layers - 1)//layers
    if per_layer <= 0:
        raise ValueError("Model memory estimate must be positive")
    runtime = gb(model["runtime_and_buffers_per_node_gb"])
    group, backend = config["trust_group"], model["backend"]
    candidates, seen, excluded = [], set(), []
    for node in config["nodes"]:
        node_id = node["id"]
        if not isinstance(node_id, str) or not node_id or node_id in seen:
            raise ValueError("Node identifiers must be nonempty unique strings")
        seen.add(node_id)
        if node.get("authorized") is not True or node.get("trust_group") != group or node.get("backend") != backend:
            excluded.append(node_id)
            continue
        budget = quota_bytes(gb(node["installed_gb"]), gb(node["available_gb"]),
                             gb(node["reserve_gb"]), node.get("percent",20),
                             gb(node["personal_cap_gb"]) if "personal_cap_gb" in node else None)
        fit = max(0, (budget-runtime)//per_layer)
        candidates.append((fit, node_id, budget))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    stages, next_layer = [], 0
    for fit, node_id, budget in candidates:
        count = min(fit, layers-next_layer)
        if count:
            stages.append(dict(node_id=node_id, layer_start=next_layer,
                               layer_end_exclusive=next_layer+count,
                               reserved_bytes=runtime+count*per_layer,
                               quota_bytes=budget))
            next_layer += count
        if next_layer == layers:
            break
    feasible = next_layer == layers
    return dict(status="planning_estimate", feasible=feasible,
                reason="complete_uniform_layer_plan" if feasible else "insufficient_authorized_capacity",
                trust_group=group, backend=backend, model=model["id"],
                stages=stages if feasible else [], excluded_nodes=excluded,
                missing_layers=layers-next_layer,
                note="No allocation or inference performed; latency and real block profiles remain to be measured.")
