from src.api.models import SummaryModel, TicketModel
from src.core.base_repository import BaseRepository


class TickerRepository(BaseRepository):
    model = TicketModel

class SummaryRepository(BaseRepository):
    model = SummaryModel