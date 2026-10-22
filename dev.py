"""
Dev server with auto-reload that works reliably on Windows.

Uses watchfiles to restart uvicorn instead of uvicorn's built-in --reload,
which often hangs on Windows because of CTRL_C_EVENT / process group quirks.
"""

import os
import sys
from pathlib import Path

from watchfiles import run_process
from watchfiles.filters import PythonFilter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

# Windows system SOCKS proxy often lands in ALL_PROXY / HTTP(S)_PROXY.
# httpx then tries SOCKS and fails (or routes LLM calls via proxy). Force direct.
_PROXY_VARS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)


def _force_direct_connections() -> None:
    for key in _PROXY_VARS:
        os.environ.pop(key, None)
    os.environ["NO_PROXY"] = "*"
    os.environ["no_proxy"] = "*"


def main() -> None:
    _force_direct_connections()
    # Use the same interpreter + -m so Windows finds uvicorn inside the venv.
    cmd = (
        f"{sys.executable} -m uvicorn main:app "
        f"--host 127.0.0.1 --port 8000"
    )
    run_process(
        SRC,
        ROOT / "main.py",
        target=cmd,
        target_type="command",
        watch_filter=PythonFilter(),
        # Give the old process a moment to release the port on Windows.
        sigint_timeout=3,
        sigkill_timeout=2,
        grace_period=0.5,
    )


if __name__ == "__main__":
    main()
