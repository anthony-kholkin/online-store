from typing import Any, TypeVar

from fastapi import Depends
from sqlalchemy import Select, func, select

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BaseModel
from db.session import get_session

MODEL = TypeVar("MODEL", bound=BaseModel)


class BaseDatabaseRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    @staticmethod
    def get_pagination_query(query: Select[tuple[Any, ...]], offset: int, limit: int) -> Select[tuple[Any, ...]]:
        return query.offset(offset).limit(limit)

    async def get_total_count(self, query: Select[tuple[Any, ...]]) -> int:
        query = select(func.count()).select_from(query.subquery())
        query_result = await self._session.execute(query)
        result = query_result.scalar_one()

        return result if result else 0
