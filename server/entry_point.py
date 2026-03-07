from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.list import router as list_router
from server.routes.user import router as user_router

from server.db.client import _get_engine
from server.db.orm_models import Base
from server.utils.logger import get_logger

_logger = get_logger(__name__)

app = FastAPI(
    title="Salsala API",
    description="Shopping list companion backend.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(list_router)


@app.on_event("startup")
async def on_startup():
    async with _get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _logger.info("Salsala API server starting up.")


@app.on_event("shutdown")
async def on_shutdown():
    _logger.info("Salsala API server shutting down.")
