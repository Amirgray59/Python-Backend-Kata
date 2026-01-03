from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.item import router as item_router
from app.api.routes.user import router as user_router
from app.db.migration.tables import create_tables 
from app.db.migration.index import create_index_mongo, create_indexes
from app.utils.logging import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    create_indexes()

    await create_index_mongo()

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
