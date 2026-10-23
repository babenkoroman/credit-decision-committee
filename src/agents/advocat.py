from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.parse import parse_vote_response
from src.agents.state import State, Vote
from src.infrastructure.llm.deepseek import get_llm


class AdvocatAgent:
    def __init__(self, application, llm=None):
        self._application = application
        self._llm = llm or get_llm()

    def __call__(self, state: State) -> dict:
        application_json = self._application.model_dump_json(indent=2)
        antifrod = next((v for v in state.votes if v.agent == "antifrod"), None)
        antifrod_text = (
            f"{antifrod.vote}: {antifrod.reason}" if antifrod else "нет заключения"
        )

        result = self._llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Ты — адвокат заявителя в кредитном комитете.\n"
                        "Оспорь или смягчи выводы антифрода. Не выдумывай данные.\n"
                        "Маппинг: защитить заявку → approve, частично согласиться → manual_review, "
                        "согласиться с антифродом → reject.\n"
                        "Ответь ТОЛЬКО JSON без markdown:\n"
                        '{"vote":"approve"|"reject"|"manual_review","reason":"контраргументы и итог"}'
                    )
                ),
                HumanMessage(
                    content=(
                        "Данные заявки и заявителя (JSON):\n"
                        f"{application_json}\n\n"
                        "Заключение антифрод-агента:\n"
                        f"{antifrod_text}"
                    )
                ),
            ]
        )

        vote, reason = parse_vote_response(result.content)
        return {"votes": [Vote(agent="advocate", vote=vote, reason=reason)]}
