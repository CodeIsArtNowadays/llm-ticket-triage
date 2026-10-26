import uuid
from datetime import datetime

from pydantic import BaseModel

from src.api.types import CategoryType, PriorityType


class TicketBaseSchema(BaseModel):
    message: str
    user: str 

class TicketRetrieveSchema(TicketBaseSchema):
    id: uuid.UUID
    created_at: datetime

class SummaryBaseSchema(BaseModel):
    summary: str
    category: CategoryType
    priority: PriorityType

class SummaryCreateSchema(SummaryBaseSchema):
    ticker_id: uuid.UUID

class TicketSummarySchema(TicketRetrieveSchema, SummaryBaseSchema):
    pass
