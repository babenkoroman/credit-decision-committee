import json
import re

ALLOWED_VOTES = {"approve", "reject", "manual_review"}


def parse_vote_response(text: str, default: str = "manual_review") -> tuple[str, str]:
    """Достаёт vote + reason из ответа LLM (JSON или строка VOTE: ...)."""
    text = (text or "").strip()
    if not text:
        return default, "Пустой ответ агента"

    # JSON-блок в markdown или сырой JSON
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            data = json.loads(match.group())
            vote = str(data.get("vote", default)).strip().lower()
            reason = str(data.get("reason", text)).strip()
            if vote not in ALLOWED_VOTES:
                vote = default
            return vote, reason or text
        except json.JSONDecodeError:
            pass

    vote_match = re.search(
        r"VOTE:\s*(approve|reject|manual_review)",
        text,
        flags=re.IGNORECASE,
    )
    if vote_match:
        return vote_match.group(1).lower(), text

    return default, text
