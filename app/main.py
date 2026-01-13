from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.item import router as item_router
from app.api.routes.user import router as user_router
from app.utils.logging import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    # shutdown

configure_logging()
app = FastAPI(lifespan=lifespan)

app.include_router(item_router)
app.include_router(user_router)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["health"])
def ready():
    return {"status": "ready"}
