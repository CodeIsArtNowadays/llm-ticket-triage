from fastapi import APIRouter, Depends

from src.api.dependencies import get_ticker_repository, get_ticket_service
from src.api.repository import TicketRepository
from src.api.schemas import TicketBaseSchema, TicketRetrieveSchema, TicketSummarySchema
from src.api.service import TicketService

api_router = APIRouter(prefix='/api')


@api_router.get('/tickets', response_model=list[TicketRetrieveSchema])
async def get_all_tickets(repo: TicketRepository = Depends(get_ticker_repository)):
    return await repo.get_all()

@api_router.post('/tickets', response_model=TicketSummarySchema)
async def create_new_ticket(ticket_data: TicketBaseSchema, service: TicketService = Depends(get_ticket_service)):
    return await service.process_ticket(ticket_data)

@api_router.get('/tickets/{id}', response_model=TicketRetrieveSchema)
async def get_ticket_by_id(id: str, repo: TicketRepository = Depends(get_ticker_repository)):
    ticket = await repo.get_by_id(id)
    print(ticket.user)
    return ticket

