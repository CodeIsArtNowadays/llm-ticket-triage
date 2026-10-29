import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.api.types import CategoryType, PriorityType
from src.core.database import Base


class TicketModel(Base):
    __tablename__ = 'tickets'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class SummaryModel(Base):
    __tablename__ = 'summaries'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    summary: Mapped[str] = mapped_column()
    category: Mapped[CategoryType] = mapped_column(String(32))
    priority: Mapped[PriorityType] = mapped_column(String(32))
    answer: Mapped[str] = mapped_column()
    error: Mapped[bool] = mapped_column(default=False)
    
    ticker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tickets.id'), unique=True)