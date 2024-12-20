from typing import Any

from sqlalchemy import select, Select, or_, func, exists, case, and_

from core.enum import OrderByEnum
from core.exceptions import no_price_type_guid_exception
from db.models import Good, GoodStorage, Price, GoodGroup
from db.models.favorites_good import favorites_goods
from db.repositories.base import BaseDatabaseRepository
from schemas.good import GoodCreateSchema


class GoodRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Good | None:
        return await self._session.get(Good, guid)

    async def is_favorite(self, cart_outlet_guid: str, good_guid: str) -> bool:
        query = select(favorites_goods).where(
            favorites_goods.c.cart_outlet_guid == cart_outlet_guid,
            favorites_goods.c.good_guid == good_guid,
        )
        result = await self._session.execute(query)
        return result.scalar() is not None

    async def merge(self, data: GoodCreateSchema) -> Good:
        good = Good(**data.model_dump(exclude_unset=True))

        await self._session.merge(good)
        await self._session.flush()

        return good

    async def add_image(self, instance: Good, image_key: str) -> None:
        instance.image_key = image_key

        await self._session.flush()

    @staticmethod
    def filter_by_in_stock(query: Select[tuple[Good, Any]], in_stock: bool) -> Select[tuple[Good, Any]]:
        if in_stock:
            filtered_query = query.join(Good.storages).filter(GoodStorage.in_stock > 0)
        else:
            filtered_query = query.outerjoin(Good.storages).filter(
                or_(GoodStorage.in_stock == 0, GoodStorage.in_stock.is_(None))
            )

        return filtered_query

    @staticmethod
    def filter_by_name(query: Select[tuple[Good, Any]], name: str) -> Select[tuple[Good, Any]]:
        search_query = func.plainto_tsquery("multi_lang", name)
        filtered_query = query.filter(func.to_tsvector("multi_lang", Good.name).op("@@")(search_query))

        return filtered_query

    @staticmethod
    def filter_by_price(
        query: Select[tuple[Good, Any]],
        price_from: float | None,
        price_to: float | None,
        price_type_guid: str | None,
    ) -> Select[tuple[Good, Any]]:
        if not price_type_guid:
            raise no_price_type_guid_exception

        subquery = select(Price.good_guid).filter(Price.price_type_guid == price_type_guid)

        if price_from is not None:
            subquery = subquery.filter(Price.value >= price_from)
        if price_to is not None:
            subquery = subquery.filter(Price.value <= price_to)

        res_subquery = subquery.distinct().subquery()

        return query.filter(Good.guid.in_(select(res_subquery.c.good_guid)))

    async def filter_by_group_guid(
        self, query: Select[tuple[Good, Any]], good_group_guids: list[str]
    ) -> Select[tuple[Good, Any]]:
        child_group_query = (
            select(GoodGroup.guid)
            .where(GoodGroup.parent_group_guid.in_(good_group_guids))
            .cte(name="child_groups", recursive=True)
        )

        recursive_part = select(GoodGroup.guid).where(GoodGroup.parent_group_guid == child_group_query.c.guid)
        child_group_query = child_group_query.union_all(recursive_part)

        all_group_guids = good_group_guids + [
            row[0] for row in (await self._session.execute(select(child_group_query.c.guid))).all()
        ]

        filtered_query = query.where(Good.good_group_guid.in_(all_group_guids))

        return filtered_query

    async def get_by_filters(
        self,
        page: int,
        size: int,
        order_by: OrderByEnum,
        in_stock: bool | None = None,
        name: str | None = None,
        price_type_guid: str | None = None,
        price_from: float | None = None,
        price_to: float | None = None,
        good_group_guids: list[str] | None = None,
        cart_outlet_guid: str | None = None,
    ) -> tuple[list[tuple[Any, Any]], int]:
        query = select(
            Good,
            case(
                (
                    exists().where(
                        and_(
                            favorites_goods.c.cart_outlet_guid == cart_outlet_guid,
                            favorites_goods.c.good_guid == Good.guid,
                        )
                    ),
                    True,
                ),
                else_=False,
            ).label("is_favorite"),
        )

        if good_group_guids is not None:
            query = await self.filter_by_group_guid(query=query, good_group_guids=good_group_guids)
        if in_stock is not None:
            query = self.filter_by_in_stock(query=query, in_stock=in_stock)
        if name is not None:
            query = self.filter_by_name(query=query, name=name)

        query = self.filter_by_price(
            query=query, price_from=price_from, price_to=price_to, price_type_guid=price_type_guid
        )

        if order_by is not None:
            match order_by:
                case OrderByEnum.TYPE:
                    query = query.order_by(Good.type)
                case OrderByEnum.NAME:
                    query = query.order_by(Good.name)
                case OrderByEnum.PRICE:
                    min_price_subq = (
                        select(Price.good_guid, func.min(Price.value).label("min_price"))
                        .where(Price.price_type_guid == price_type_guid)
                        .group_by(Price.good_guid)
                        .subquery()
                    )

                    query = query.join(min_price_subq, Good.guid == min_price_subq.c.good_guid)
                    query = query.add_columns(min_price_subq.c.min_price)
                    query = query.order_by(min_price_subq.c.min_price.desc())

        query = query.distinct()
        count = await self.get_total_count(query=query)

        query = self.get_pagination_query(query=query, offset=(page - 1) * size, limit=size)

        query_result = await self._session.execute(query)

        if order_by == "price":
            processed_result = [(row[0], row[1]) for row in query_result.all()]
        else:
            processed_result = query_result.all()

        return list(processed_result), count
