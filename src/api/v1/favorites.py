from fastapi import APIRouter, status, Security, Path, Depends, Query

from schemas.favorites import GetFavoritesSchema
from schemas.outlet import OutletSchema
from services.auth import verify_token_outlets
from services.web.favorites import FavoritesService

router = APIRouter(prefix="/outlets", tags=["Избранное"])


@router.get(
    "/{cart_outlet_guid}/favorites",
    status_code=status.HTTP_200_OK,
    response_model=GetFavoritesSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def get_favorites_by_outlet_guid(
    cart_outlet_guid: str = Path(...),
    price_type_guid: str = Query(...),
    favorites_service: FavoritesService = Depends(),
) -> GetFavoritesSchema:
    return await favorites_service.get_favorites(cart_outlet_guid=cart_outlet_guid, price_type_guid=price_type_guid)
