from typing import Sequence

from fastapi import APIRouter, status, Depends

from db.models import GoodGroup
from schemas.good_group import GoodGroupSchema
from services.auth import authenticate
from services.lc.good_group import GoodGroupService

router = APIRouter(prefix="/good_groups", tags=["1C Группы товаров"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=GoodGroupSchema, dependencies=[Depends(authenticate)]
)
async def create_good_group(
    data: GoodGroupSchema,
    good_group_service: GoodGroupService = Depends(),
) -> GoodGroup:
    return await good_group_service.create_or_update(data=data)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[GoodGroupSchema], dependencies=[Depends(authenticate)]
)
async def get_good_groups(
    good_group_service: GoodGroupService = Depends(),
) -> Sequence[GoodGroup]:
    return await good_group_service.get_all()


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=GoodGroupSchema, dependencies=[Depends(authenticate)]
)
async def get_good_group_by_id(
    guid: str,
    good_group_service: GoodGroupService = Depends(),
) -> GoodGroup:
    return await good_group_service.get_by_guid(guid=guid)


# @router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
# async def delete_good_by_id(
#     guid: str,
#     good_group_service: GoodGroupService = Depends(),
# ) -> None:
#     return await good_group_service.delete(guid=guid)
