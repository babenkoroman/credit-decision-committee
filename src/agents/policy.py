from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import State
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
                        "Ты кредитный комитет. Решай строго по политикам компании ниже. "
                        "Учитывай только сумму кредита и текст политик — другие факторы не выдумывай. "
                        "Ответ кратко: "
                        "1) решение: одобрено / условно одобрено со снижением / отказ; "
                        "2) итоговый лимит в рублях, если применимо; "
                        "3) обоснование в 2–3 предложениях со ссылкой на сегмент политики."
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

        return {"summary": f"{state.summary} {result.content}".strip()}
