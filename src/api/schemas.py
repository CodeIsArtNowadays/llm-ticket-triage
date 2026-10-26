import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from src.api.types import CategoryType, PriorityType


class TicketBaseSchema(BaseModel):
    message: Annotated[str, StringConstraints(min_length=5, strip_whitespace=True)]
    user: Annotated[str, StringConstraints(min_length=5, strip_whitespace=True)]

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
