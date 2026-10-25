from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router

from src.core.database import Base, engine
from src.api.models import TicketModel, SummaryModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Исправление ошибки для AsyncEngine:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    # Действия при остановке приложения (если необходимы)

app = FastAPI(lifespan=lifespan)


app.include_router(api_router)
