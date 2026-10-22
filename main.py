import uvicorn
from fastapi import FastAPI

from src.api.routes import router
from src.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)
app.include_router(router, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
