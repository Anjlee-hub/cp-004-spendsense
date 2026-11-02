
from decimal import Decimal, InvalidOperation


THRESHOLDS = {
    80: Decimal("0.80"),
    100: Decimal("1.00")
}


def to_decimal(value):
    """Convert a value to Decimal safely."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

    if not result.is_finite():
        raise ValueError("Amount must be finite.")

    return result


def calculate_utilization(spending, budget):
    """Calculate budget utilization percentage."""
    spending = to_decimal(spending)
    budget = to_decimal(budget)

    if spending < 0:
        raise ValueError("Spending cannot be negative.")

    if budget < 0:
        raise ValueError("Budget cannot be negative.")

    if budget == 0:
        return Decimal("0") if spending == 0 else Decimal("Infinity")

    return (spending / budget) * Decimal("100")


def check_budget_thresholds(
    month,
    category,
    previous_spending,
    updated_spending,
    budget
):
    """
    Return alerts when spending crosses 80% or 100%.

    Alerts are emitted only when a threshold is crossed
    from below to at or above the threshold.
    """

    previous_spending = to_decimal(previous_spending)
    updated_spending = to_decimal(updated_spending)
    budget = to_decimal(budget)

    if previous_spending < 0 or updated_spending < 0:
        raise ValueError("Spending cannot be negative.")

    if budget <= 0:
        return []

    if updated_spending < previous_spending:
        raise ValueError(
            "Updated spending cannot be lower than previous spending."
        )

    alerts = []

    for threshold, ratio in THRESHOLDS.items():
        threshold_amount = budget * ratio

        if (
            previous_spending < threshold_amount
            and updated_spending >= threshold_amount
        ):
            alerts.append({
                "month": month,
                "category": category,
                "threshold": threshold,
                "message": (
                    f"ALERT: {category} budget has reached "
                    f"{threshold}% for {month}."
                )
            })

    return alerts
