from fastapi import APIRouter, status, Depends, Query
from schemas.good_group import GetTreeGoodGroupSchema
from services.web.good_group import GoodGroupService

router = APIRouter(prefix="/good-groups", tags=["Группы товаров"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[GetTreeGoodGroupSchema])
async def get_good_by_id(
    good_service: GoodGroupService = Depends(), price_type_guid: str = Query(...)
) -> list[GetTreeGoodGroupSchema]:
    return await good_service.get_available_good_groups(price_type_guid=price_type_guid)
