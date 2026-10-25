from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repository import TickerRepository
from src.core.database import get_db


def get_ticker_repository(session: AsyncSession = Depends(get_db)):
    return TickerRepository(session)