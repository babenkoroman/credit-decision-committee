from langchain_deepseek import ChatDeepSeek

from src.config import settings

_llm: ChatDeepSeek | None = None

def get_llm() -> ChatDeepSeek:
    global _llm
    if _llm is None:
        _llm = ChatDeepSeek(
            model="deepseek-flash",
            api_key=settings.deepseek_api_key,
        )
    return _llm
