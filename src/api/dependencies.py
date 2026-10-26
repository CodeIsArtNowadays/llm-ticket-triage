from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repository import SummaryRepository, TicketRepository
from src.api.service import TicketService
from src.core.database import get_db


def get_ticker_repository(session: AsyncSession = Depends(get_db)):
    return TicketRepository(session)

def get_summary_repository(session: AsyncSession = Depends(get_db)):
    return SummaryRepository(session)

def get_ticket_service(
    ticket_repo: TicketRepository = Depends(get_ticker_repository),
    summary_repo: SummaryRepository = Depends(get_summary_repository)
):
    return TicketService(ticket_repo=ticket_repo, summary_repo=summary_repo)