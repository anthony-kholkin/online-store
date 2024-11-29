from fastapi import APIRouter, status, Security, Depends, Path, Query

from db.models import Cart
from schemas.cart import GetCartSchema, AddOrUpdateGoodToCartSchema, GetBaseCartSchema, CartGoodSchema, DeleteGoodSchema
from schemas.outlet import OutletSchema
from services.auth import verify_token
from services.web.cart import CartService

router = APIRouter(prefix="/outlets", tags=["Торговый точки"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[OutletSchema],
)
async def get_outlets(outlets: list[OutletSchema] = Security(verify_token)) -> list[OutletSchema]:
    return outlets


@router.get(
    "/{cart_outlet_guid}/cart",
    status_code=status.HTTP_200_OK,
    response_model=GetCartSchema,
    dependencies=[Security(verify_token)],
)
async def get_cart_by_outlet_guid(
    cart_outlet_guid: str = Path(...),
    cart_service: CartService = Depends(),
) -> GetCartSchema:
    return await cart_service.get_cart(cart_outlet_guid=cart_outlet_guid)


@router.post(
    "/{cart_outlet_guid}/cart",
    status_code=status.HTTP_200_OK,
    response_model=GetBaseCartSchema,
    dependencies=[Security(verify_token)],
)
async def add_good_to_cart(
    data: AddOrUpdateGoodToCartSchema,
    cart_outlet_guid: str = Path(),
    cart_service: CartService = Depends(),
) -> Cart:
    return await cart_service.add_good(cart_outlet_guid=cart_outlet_guid, data=data)


@router.delete(
    "/{cart_outlet_guid}/cart",
    status_code=status.HTTP_200_OK,
    response_model=DeleteGoodSchema,
    dependencies=[Security(verify_token)],
)
async def delete_good_from_cart(
    cart_outlet_guid: str = Path(),
    good_guid: str = Query(),
    specification_guid: str = Query(),
    cart_service: CartService = Depends(),
) -> DeleteGoodSchema:
    return await cart_service.delete_good(
        cart_outlet_guid=cart_outlet_guid,
        good_guid=good_guid,
        specification_guid=specification_guid,
    )


@router.put(
    "/{cart_outlet_guid}/cart",
    status_code=status.HTTP_201_CREATED,
    response_model=CartGoodSchema,
    dependencies=[Security(verify_token)],
)
async def update_good_quantity(
    data: AddOrUpdateGoodToCartSchema,
    cart_outlet_guid: str = Path(),
    cart_service: CartService = Depends(),
) -> CartGoodSchema:
    return await cart_service.update_good_count_in_cart(cart_outlet_guid=cart_outlet_guid, data=data)
