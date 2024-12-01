from typing import Sequence

from sqlalchemy import select, Select, or_, func

from core.exceptions import no_price_type_guid_exception
from db.models import Good, GoodStorage, Price
from db.repositories.base import BaseDatabaseRepository
from schemas.good import GoodCreateSchema


class GoodRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Good | None:
        return await self._session.get(Good, guid)

    async def merge(self, data: GoodCreateSchema) -> Good:
        good = Good(**data.model_dump(exclude_unset=True))

        await self._session.merge(good)
        await self._session.flush()

        return good

    async def add_image(self, instance: Good, image_key: str) -> None:
        instance.image_key = image_key

        await self._session.flush()

    @staticmethod
    def filter_by_in_stock(query: Select[tuple[Good]], in_stock: bool) -> Select[tuple[Good]]:
        if in_stock:
            filtered_query = query.join(Good.storages).filter(GoodStorage.in_stock > 0)
        else:
            filtered_query = query.outerjoin(Good.storages).filter(
                or_(GoodStorage.in_stock == 0, GoodStorage.in_stock.is_(None))
            )

        return filtered_query

    @staticmethod
    def filter_by_name(query: Select[tuple[Good]], name: str) -> Select[tuple[Good]]:
        search_query = func.plainto_tsquery("multi_lang", name)
        filtered_query = query.filter(func.to_tsvector("multi_lang", Good.name).op("@@")(search_query))

        return filtered_query

    @staticmethod
    def filter_by_price(
        query: Select[tuple[Good]],
        price_from: float | None,
        price_to: float | None,
        price_type_guid: str | None,
    ) -> Select[tuple[Good]]:
        if not price_type_guid:
            raise no_price_type_guid_exception

        subquery = select(Price.good_guid).filter(Price.price_type_guid == price_type_guid)

        if price_from is not None:
            subquery = subquery.filter(Price.value >= price_from)
        if price_to is not None:
            subquery = subquery.filter(Price.value <= price_to)

        res_subquery = subquery.distinct().subquery()

        return query.filter(Good.guid.in_(select(res_subquery.c.good_guid)))

    async def get_by_filters(
        self,
        page: int,
        size: int,
        in_stock: bool | None = None,
        name: str | None = None,
        price_type_guid: str | None = None,
        price_from: float | None = None,
        price_to: float | None = None,
    ) -> tuple[Sequence[Good], int]:
        query = select(Good)

        if in_stock is not None:
            query = self.filter_by_in_stock(query=query, in_stock=in_stock)
        if name is not None:
            query = self.filter_by_name(query=query, name=name)

        query = self.filter_by_price(
            query=query, price_from=price_from, price_to=price_to, price_type_guid=price_type_guid
        )

        count = await self._session.scalar(select(func.count()).select_from(query.subquery()))
        count = count if count else 0

        query = query.distinct(Good.guid)
        query = self.get_pagination_query(query=query, offset=(page - 1) * size, limit=size)

        query_result = await self._session.execute(query)
        return query_result.scalars().all(), count
