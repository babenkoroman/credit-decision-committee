from src.agents.state import Vote
from src.rules.hard_stops import risk_decision


def aggregate_decision(votes: list[Vote], credit_sum: float | None) -> str:
    """Сводит голоса + hard-stop."""
    if risk_decision(credit_sum) == "reject":
        return "reject"

    by_agent = {v.agent: v for v in votes}

    risk = by_agent.get("risk")
    if risk and risk.vote == "reject":
        return "reject"

    policy = by_agent.get("policy")
    if policy and policy.vote == "reject":
        return "reject"

    antifrod = by_agent.get("antifrod")
    if antifrod and antifrod.vote == "reject":
        advocate = by_agent.get("advocate")
        if advocate and advocate.vote == "approve":
            return "manual_review"
        return "reject"

    if not votes:
        return "manual_review"

    values = [v.vote for v in votes]
    if all(v == "approve" for v in values):
        return "approve"
    if "manual_review" in values:
        return "manual_review"
    if values.count("approve") > values.count("reject"):
        return "approve"
    if values.count("reject") > values.count("approve"):
        return "reject"
    return "manual_review"
