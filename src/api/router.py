from fastapi import APIRouter, Depends

from src.api.dependencies import get_ticker_repository
from src.api.repository import TickerRepository

api_router = APIRouter(prefix='/api')


@api_router.get('/tickets')
async def get_all_tickets(repo: TickerRepository = Depends(get_ticker_repository)):
    return await repo.get_all()


