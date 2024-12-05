
from fastapi import APIRouter, status, Depends
from schemas.good_group import GetGoodGroupSchema
from services.web.good_group import GoodGroupService

router = APIRouter(prefix="/good-groups", tags=["Группы товаров"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[GetGoodGroupSchema])
async def get_good_by_id(
    good_service: GoodGroupService = Depends(),
) -> list[GetGoodGroupSchema]:
    return await good_service.get_available_good_groups()
