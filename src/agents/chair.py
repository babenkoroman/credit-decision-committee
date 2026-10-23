from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import State
from src.infrastructure.llm.deepseek import get_llm
from src.rules.chair import aggregate_decision


class ChairAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        decision = aggregate_decision(
            state.votes,
            self._application.credit_sum,
        )

        votes_json = "\n".join(
            f"- {v.agent}: {v.vote} — {v.reason}" for v in state.votes
        ) or "голосов нет"

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — председатель кредитного комитета. "
                        "Решение уже принято правилами комитета — НЕ меняй его. "
                        "Напиши краткое memo (3–5 предложений) для аудита: "
                        "почему такое решение, опираясь на голоса агентов."
                    )
                ),
                HumanMessage(
                    content=(
                        f"Итоговое решение (фиксировано): {decision}\n\n"
                        f"Голоса агентов:\n{votes_json}"
                    )
                ),
            ]
        )

        return {
            "decision": decision,
            "memo": result.content.strip(),
        }
