from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes.item import router as item_router 
from app.api.routes.user import router as user_router

from app.utils.logging import configure_logging
from app.api.deps import create_tables

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

    create_tables()
    
    app.include_router(item_router)
    app.include_router(user_router)
    

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    @app.get("/ready", tags=["health"])
    def ready():
        return {"status": "ready"}

    return app


app = create_app()
