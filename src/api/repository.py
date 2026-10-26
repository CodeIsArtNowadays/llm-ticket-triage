import uuid

from sqlalchemy import select

from src.api.models import SummaryModel, TicketModel
from src.core.base_repository import BaseRepository
from src.core.exceptions import NotFoundException


class TicketRepository(BaseRepository):
    model = TicketModel

class SummaryRepository(BaseRepository):
    model = SummaryModel

    async def get_by_ticket_id(self, id: uuid.UUID):
        stmt = select(SummaryModel).where(SummaryModel.ticker_id == id)
        res = await self.session.scalar(stmt)

        if res is None:
            raise NotFoundException(message=f'{self.model} with ticket_id {id} not found')

        return res