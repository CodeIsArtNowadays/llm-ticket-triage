from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar('ModelType')

class BaseRepository[ModelType]:

    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data):
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id):
        res = await self.session.get(self.model, id)
        return res

    async def get_all(self):
        stmt = select(self.model)
        res = await self.session.scalars(stmt)
        return res.all()

    
        