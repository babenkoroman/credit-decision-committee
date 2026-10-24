import httpx
from langchain_deepseek import ChatDeepSeek

from src.config import settings
from src.infrastructure.no_proxy import disable_system_proxies

_llm: ChatDeepSeek | None = None


def get_llm() -> ChatDeepSeek:
    global _llm
    disable_system_proxies()
    if _llm is None:
        _llm = ChatDeepSeek(
            model="deepseek-flash",
            api_key=settings.deepseek_api_key,
            http_client=httpx.Client(trust_env=False),
            http_async_client=httpx.AsyncClient(trust_env=False),
        )
    return _llm
