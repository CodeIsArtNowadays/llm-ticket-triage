import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from src.api.types import CategoryType, PriorityType


class TicketBaseSchema(BaseModel):
    message: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    user: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]

class TicketRetrieveSchema(TicketBaseSchema):
    id: uuid.UUID
    created_at: datetime

class SummaryBaseSchema(BaseModel):
    summary: str
    category: CategoryType
    priority: PriorityType
    answer: str
    error: bool = Field(default=False)

class SummaryCreateSchema(SummaryBaseSchema):
    ticker_id: uuid.UUID

class TicketSummarySchema(TicketRetrieveSchema, SummaryBaseSchema):
    pass
