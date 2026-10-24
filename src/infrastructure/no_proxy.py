"""Force direct outbound HTTP — ignore system/VPN proxy env vars."""

from __future__ import annotations

import os

_PROXY_ENV_VARS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)


def disable_system_proxies() -> None:
    for name in _PROXY_ENV_VARS:
        os.environ.pop(name, None)
