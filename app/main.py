from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes import router as items_router
from app.utils.logging import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


def create_app():
    configure_logging()
    app = FastAPI(
        lifespan=lifespan,
    )

    app.include_router(items_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    @app.get("/ready", tags=["health"])
    def ready():
        return {"status": "ready"}

    return app


app = create_app()
