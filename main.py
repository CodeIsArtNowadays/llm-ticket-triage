from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.models import SummaryModel, TicketModel
from src.api.router import api_router
from src.core.database import Base, engine
from src.core.exceptions import ProjectBaseException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Исправление ошибки для AsyncEngine:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    # Действия при остановке приложения (если необходимы)

app = FastAPI(lifespan=lifespan)


app.include_router(api_router)

@app.exception_handler(ProjectBaseException)
async def exception_handler(request: Request, exc):
    return JSONResponse(content=exc.message, status_code=exc.status_code)
