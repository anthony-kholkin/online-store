from fastapi import APIRouter, status, Security

from schemas.outlet import OutletSchema
from services.auth import verify_token_outlets


router = APIRouter(prefix="/outlets", tags=["Торговый точки"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[OutletSchema],
)
async def get_outlets(outlets: list[OutletSchema] = Security(verify_token_outlets)) -> list[OutletSchema]:
    return outlets
