from fastapi import APIRouter

from api.v1.lc.good_group import router as lc_good_group_router
from api.v1.lc.good import router as lc_good_router
from api.v1.lc.specification import router as lc_specification_router
from api.v1.lc.good_storage import router as lc_good_storage_router
from api.v1.lc.price_type import router as lc_price_type_router
from api.v1.lc.price import router as lc_price_router

from api.v1.good import router as good_router
from api.v1.auth import router as auth_router
from api.v1.contact_me import router as contact_me_router
from api.v1.outlet import router as outlet_router
from api.v1.cart import router as cart_router
from api.v1.favorites import router as favorites_router

lc_router = APIRouter(prefix="/1c")
lc_router.include_router(lc_good_group_router)
lc_router.include_router(lc_good_router)
lc_router.include_router(lc_good_storage_router)
lc_router.include_router(lc_specification_router)
lc_router.include_router(lc_price_type_router)
lc_router.include_router(lc_price_router)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(lc_router)
v1_router.include_router(good_router)
v1_router.include_router(auth_router)
v1_router.include_router(contact_me_router)
v1_router.include_router(outlet_router)
v1_router.include_router(cart_router)
v1_router.include_router(favorites_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
