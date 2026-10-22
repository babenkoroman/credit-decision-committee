MAX_CREDIT_SUM = 200_000


def risk_decision(credit_sum: float) -> str:
    """Yes — риск приемлем, No — отказ по порогу суммы."""
    if credit_sum > MAX_CREDIT_SUM:
        return "No"
    return "Yes"
