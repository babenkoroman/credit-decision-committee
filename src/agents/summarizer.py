from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import State
from src.infrastructure.llm.deepseek import get_llm


class SummarizerAgent:
    def __init__(self, llm=None):
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — итоговый саммаризатор кредитного комитета. "
                        "На основе результатов всех агентов реши: дать кредит или отказать. "
                        "Объясни решение кратко."
                    )
                ),
                HumanMessage(
                    content=(
                        "Результаты работы агентов (JSON):\n"
                        f"{state.model_dump_json(indent=2)}"
                    )
                ),
            ]
        )

        return {"result": result.content}
