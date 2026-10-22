from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import State
from src.infrastructure.llm.deepseek import get_llm


class AntifrodAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        application_json = self._application.model_dump_json(indent=2)

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — антифрод-аналитик кредитного комитета.\n"
                        "Твоя задача — оценить заявку на признаки мошенничества или "
                        "недобросовестного поведения и дать рекомендацию.\n\n"
                        "Опирайся только на переданные данные о заявке и заявителе. "
                        "Не выдумывай факты, которых нет во входных данных.\n\n"
                        "Формат ответа:\n"
                        "1) решение: низкий риск / средний риск / высокий риск;\n"
                        "2) рекомендация: одобрить / доп. проверка / отказать;\n"
                        "3) обоснование в 2–3 предложениях с указанием конкретных сигналов."
                    )
                ),
                HumanMessage(
                    content=(
                        "Данные заявки и заявителя (JSON):\n"
                        f"{application_json}"
                    )
                ),
            ]
        )

        return {"antifrod_agent_decision": result.content}
