from datetime import datetime
from decimal import Decimal
from enum import IntEnum

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class DiscountStatus(IntEnum):
    BASE = 0
    BRONZE = 5
    SILVER = 15
    GOLD = 30


class ClientModel(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    status: Mapped[DiscountStatus] = mapped_column(Integer, default=DiscountStatus.BASE)


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )