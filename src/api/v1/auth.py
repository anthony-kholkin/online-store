from fastapi import APIRouter, status, Depends, Request
from starlette.responses import Response

from schemas.auth import LoginSchema
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def create_auth_session(
    data: LoginSchema,
    auth_service: AuthService = Depends(),
) -> Response:
    return await auth_service.create_token(data=data)


@router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def delete_auth_session(
    request: Request,
    auth_service: AuthService = Depends(),
) -> Response:
    return await auth_service.delete_token(token=request.cookies.get("token"))
