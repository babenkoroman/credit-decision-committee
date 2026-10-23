MAX_CREDIT_SUM = 200_000


def risk_decision(credit_sum: float | None) -> str:
    """approve | reject | manual_review — детерминированный порог по сумме."""
    if credit_sum is None:
        return "manual_review"
    if credit_sum > MAX_CREDIT_SUM:
        return "reject"
    return "approve"
