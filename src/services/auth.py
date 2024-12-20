import base64
import json
from json import JSONDecodeError

import aiohttp
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse, Response
from fastapi import Depends, Cookie, Query, Path, HTTPException, status

from core.config import settings
from core.constants import RETAIL_PRICE_TYPE
from core.exceptions import (
    invalid_creds_exception,
    outlets_validate_exception,
    outlets_json_decode_exception,
    outlets_1c_error_exception,
    no_auth_exception,
    expired_token_exception,
    access_denied_exception, no_connection_exception,
)
from db.repositories.outlet import OutletRedisRepository
from schemas.auth import LoginSchema
from schemas.outlet import OutletSchema
from services.web.outlet import OutletService


class AuthService:
    def __init__(
            self,
            outlet_repository: OutletRedisRepository = Depends(),
            outlet_service: OutletService = Depends(),
    ):
        self._outlet_repository = outlet_repository
        self._outlet_service = outlet_service
        self._serializer = URLSafeTimedSerializer(settings().AUTH_SECRET)

    async def _load_and_verify_token(self, token: str | None) -> list[OutletSchema]:
        if not token:
            raise no_auth_exception

        try:
            self._serializer.loads(token, salt=settings().AUTH_SALT, max_age=settings().TOKEN_EXPIRATION_TIME)
        except SignatureExpired:
            raise expired_token_exception
        except BadSignature:
            raise no_auth_exception

        return await self._outlet_service.get_all_by_token(token=token)

    async def create_token(self, data: LoginSchema) -> Response:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(settings().auth_login_1c_url, json=data.model_dump()) as client_response:
                    response_data = await client_response.text()
                    logger.info(f"{data.model_dump_json()=}")
                    logger.info(f"{response_data=}")

                    if "403" in response_data:
                        logger.error(f"{invalid_creds_exception.detail}")
                        raise invalid_creds_exception
                    elif "[" and "]" in response_data:
                        token = self._serializer.dumps(data.login, salt=settings().AUTH_SALT)

                        try:
                            data_list = json.loads(response_data)
                            outlets = [OutletSchema(**item) for item in data_list]
                        except JSONDecodeError:
                            raise outlets_json_decode_exception
                        except ValidationError:
                            raise outlets_validate_exception

                        await self._outlet_service.set_list(
                            token=token, outlets=outlets, expiration_seconds=settings().TOKEN_EXPIRATION_TIME
                        )

                        json_response = JSONResponse(content="Login successful")
                        json_response.set_cookie(key="token", value=token, httponly=True)

                        return json_response
                    else:
                        raise outlets_1c_error_exception
            except aiohttp.client_exceptions.ClientConnectorError:
                raise no_connection_exception

    async def delete_token(self, token: str | None) -> Response:
        if not token:
            raise invalid_creds_exception

        await self._outlet_repository.delete(token=token)

        json_response = JSONResponse(content="Logout successful")
        json_response.set_cookie(key="token", value=token, httponly=True)

        return json_response

    async def verify_token_outlets(
            self,
            token: str | None = Cookie(default=None),
    ) -> list[OutletSchema]:
        return await self._load_and_verify_token(token=token)

    async def verify_token_cart(
            self,
            token: str | None = Cookie(default=None),
            cart_outlet_guid: str = Path(...),
    ) -> OutletSchema | list[OutletSchema]:
        outlets = await self._load_and_verify_token(token=token)

        if cart_outlet_guid:
            outlet = next((o for o in outlets if o.guid == cart_outlet_guid), None)
            if not outlet:
                raise access_denied_exception
            return outlet

        return outlets

    async def verify_token_goods(
            self, price_type_guid: str = Query(...), token: str | None = Cookie(default=None)
    ) -> None:
        if price_type_guid == RETAIL_PRICE_TYPE:
            return

        outlets = await self._load_and_verify_token(token=token)

        if price_type_guid != RETAIL_PRICE_TYPE and not any(
                outlet.price_type_guid == price_type_guid for outlet in outlets
        ):
            raise access_denied_exception


def get_auth_service(
        outlet_repository: OutletRedisRepository = Depends(),
        outlet_service: OutletService = Depends(),
) -> AuthService:
    return AuthService(outlet_repository=outlet_repository, outlet_service=outlet_service)


async def verify_token_outlets(
        token: str = Cookie(None, include_in_schema=False),
        auth_service: AuthService = Depends(get_auth_service),
) -> list[OutletSchema] | OutletSchema | None:
    return await auth_service.verify_token_outlets(token=token)


async def verify_token_cart(
        token: str = Cookie(None, include_in_schema=False),
        auth_service: AuthService = Depends(get_auth_service),
        cart_outlet_guid: str = Path(...),
) -> list[OutletSchema] | OutletSchema | None:
    return await auth_service.verify_token_cart(token=token, cart_outlet_guid=cart_outlet_guid)


async def verify_token_goods(
        auth_service: AuthService = Depends(get_auth_service),
        price_type_guid: str = Query(default=RETAIL_PRICE_TYPE),
        token: str | None = Cookie(default=None, include_in_schema=False),
) -> None:
    return await auth_service.verify_token_goods(price_type_guid=price_type_guid, token=token)


security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    encoded_credentials = f"{credentials.username}:{credentials.password}".encode("utf-8")
    token = base64.b64encode(encoded_credentials).decode("utf-8")

    if credentials.username != settings().AUTH_1C_LOGIN or credentials.password != settings().AUTH_1C_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return token
