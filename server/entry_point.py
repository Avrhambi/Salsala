from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes import item, list, receipt, store, transaction
from server.utils.logger import get_logger

_logger = get_logger(__name__)

app = FastAPI(
    title="Salsala API",
    description="Intelligent Hebrew shopping companion backend.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(list.router)
app.include_router(item.router)
app.include_router(transaction.router)
app.include_router(receipt.router)
app.include_router(store.router)


@app.on_event("startup")
async def on_startup():
    _logger.info("Salsala API server starting up.")


@app.on_event("shutdown")
async def on_shutdown():
    _logger.info("Salsala API server shutting down.")
