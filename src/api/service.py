import uuid

from src.api.models import SummaryModel, TicketModel
from src.api.repository import SummaryRepository, TicketRepository
from src.api.schemas import (
    SummaryCreateSchema,
    TicketBaseSchema,
    TicketRetrieveSchema,
    TicketSummarySchema,
)


def mock_ai(ticket_data: TicketRetrieveSchema) -> SummaryCreateSchema:
    return SummaryCreateSchema(
        summary='summary1',
        category='billing',
        priority='low',
        ticker_id=ticket_data.id
    )

class TicketService:

    def __init__(self, ticket_repo: TicketRepository, summary_repo: SummaryRepository):
        self.ticket_repo = ticket_repo
        self.summary_repo = summary_repo

    async def create_ticket(self, ticket_data: TicketBaseSchema) -> TicketModel:
        return await self.ticket_repo.create(ticket_data)

    async def create_summary(self, summary_data: SummaryCreateSchema) -> SummaryModel:
        return await self.summary_repo.create(summary_data)

    async def create_ticket_summary_schema(self, ticket: TicketModel, summary: SummaryModel):
        return TicketSummarySchema(
            id=ticket.id,
            created_at=ticket.created_at,
            user=ticket.user,
            message=ticket.message,
            summary=summary.summary,
            category=summary.category,
            priority=summary.priority
        )
    
    async def process_ticket(self, ticket_data: TicketBaseSchema):
        ticket = await self.create_ticket(ticket_data)
        summary_from_ai = mock_ai(ticket)
        summary = await self.create_summary(summary_from_ai)

        return await self.create_ticket_summary_schema(ticket, summary)

    async def get_ticket_summary_by_id(self, id: uuid.UUID) -> TicketSummarySchema:
        ticket = await self.ticket_repo.get_by_id(id)
        summary = await self.summary_repo.get_by_ticket_id(id)

        return await self.create_ticket_summary_schema(ticket, summary)
