"""Memory admission arithmetic, not OS enforcement. Units are bytes."""
from decimal import Decimal, InvalidOperation

def number(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name}: a boolean is not a number")
    try:
        out = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{name}: invalid number") from exc
    if not out.is_finite() or out < 0:
        raise ValueError(f"{name}: must be finite and nonnegative")
    return out

def gb(value):
    return int(number(value, "GB") * 1_000_000_000)

def quota_bytes(installed, available, reserve, percent=20, personal_cap=None):
    """Snapshot before admission. Do not repeatedly subtract our own allocation.

    For an already running agent the caller must provide a normalized capacity
    estimate, taking care not to count reclaimable memory twice.
    """
    total = number(installed, "installed")
    free = number(available, "available")
    comfort = number(reserve, "reserve")
    pct = number(percent, "percent")
    cap = total if personal_cap is None else number(personal_cap, "personal_cap")
    if free > total or pct > 100:
        raise ValueError("available must not exceed installed; percent must be <= 100")
    return int(max(Decimal(0), min(total*pct/100, free-comfort, cap)))
