from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.state import State
from src.infrastructure.llm.deepseek import get_llm


class AdvocatAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        application_json = self._application.model_dump_json(indent=2)

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — адвокат заявителя в кредитном комитете.\n"
                        "Твоя задача — защитить интересы клиента: оспорить или смягчить "
                        "выводы антифрод-агента, опираясь на те же данные заявки.\n\n"
                        "Не отрицай факты без оснований. Ищи альтернативные объяснения, "
                        "смягчающие обстоятельства и аргументы в пользу выдачи кредита.\n"
                        "Не выдумывай данные, которых нет во входе.\n\n"
                        "Формат ответа:\n"
                        "1) позиция: защитить заявку / частично согласиться / согласиться с антифродом;\n"
                        "2) контраргументы к ключевым пунктам антифрод-решения;\n"
                        "3) итог в 2–3 предложениях: почему кредит всё же можно рассмотреть."
                    )
                ),
                HumanMessage(
                    content=(
                        "Данные заявки и заявителя (JSON):\n"
                        f"{application_json}\n\n"
                        "Заключение антифрод-агента:\n"
                        f"{state.antifrod_agent_decision}"
                    )
                ),
            ]
        )

        return {"advocate_agent_decision": result.content}
