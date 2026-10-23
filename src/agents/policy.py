from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.parse import parse_vote_response
from src.agents.state import State, Vote
from src.infrastructure.llm.deepseek import get_llm
from src.infrastructure.rag.chroma import search_policy


class PolicyAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        credit_sum = self._application.credit_sum

        documents = search_policy(credit_sum)
        policies = "\n\n".join(
            f"[Политика {i}]\n{doc}" for i, doc in enumerate(documents, start=1)
        ) or "Релевантные политики не найдены."

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты агент кредитной политики. Решай строго по политикам ниже. "
                        "Учитывай только сумму кредита и текст политик.\n"
                        "Ответь ТОЛЬКО JSON без markdown:\n"
                        '{"vote":"approve"|"reject"|"manual_review","reason":"2-3 предложения со ссылкой на сегмент"}'
                    )
                ),
                HumanMessage(
                    content=(
                        f"Сумма запрашиваемого кредита: {credit_sum} рублей.\n\n"
                        f"Найденные политики:\n{policies}"
                    )
                ),
            ]
        )

        vote, reason = parse_vote_response(result.content)
        return {"votes": [Vote(agent="policy", vote=vote, reason=reason)]}
