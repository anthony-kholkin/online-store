from fastapi import APIRouter, status, Security, Path, Depends, Query

from db.models import Favorites
from schemas.favorites import GetFavoritesSchema, BaseFavoritesSchema, DeleteFavoritesSchema
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


@router.post(
    "/{cart_outlet_guid}/favorites",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseFavoritesSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def add_good_to_favorites(
    cart_outlet_guid: str = Path(...),
    good_guid: str = Query(...),
    favorites_service: FavoritesService = Depends(),
) -> Favorites:
    return await favorites_service.add_good(cart_outlet_guid=cart_outlet_guid, good_guid=good_guid)


@router.delete(
    "/{cart_outlet_guid}/favorites",
    status_code=status.HTTP_200_OK,
    response_model=DeleteFavoritesSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def delete_good_from_favorites(
    cart_outlet_guid: str = Path(...),
    good_guid: str = Query(...),
    favorites_service: FavoritesService = Depends(),
) -> DeleteFavoritesSchema:
    return await favorites_service.delete_good(
        cart_outlet_guid=cart_outlet_guid,
        good_guid=good_guid,
    )
