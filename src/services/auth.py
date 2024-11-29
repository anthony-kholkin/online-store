import json
from json import JSONDecodeError

import aiohttp
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse, Response
from fastapi import Depends, Cookie

from core.config import settings
from core.constants import RETAIL_PRICE_TYPE
from core.exceptions import (
    invalid_creds_exception,
    outlets_validate_exception,
    outlets_json_decode_exception,
    outlets_1c_error_exception,
    no_auth_exception,
    expired_token_exception,
    access_denied_exception,
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

    async def create_token(self, data: LoginSchema) -> Response:
        async with aiohttp.ClientSession() as session:
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

    async def delete_token(self, token: str | None) -> Response:
        if not token:
            raise invalid_creds_exception

        await self._outlet_repository.delete(token=token)

        json_response = JSONResponse(content="Logout successful")
        json_response.set_cookie(key="token", value=token, httponly=True)

        return json_response

    async def verify_token(
        self,
        token: str | None,
        cart_outlet_guid: str | None = None,
        price_type_guid: str | None = None,
    ) -> list[OutletSchema] | OutletSchema | None:
        """
        Универсальная проверка токена и сопоставление
        с дополнительными параметрами (cart_outlet_guid или price_type_guid).
        """
        if price_type_guid == RETAIL_PRICE_TYPE:
            return None

        if not token:
            raise no_auth_exception

        try:
            self._serializer.loads(token, salt=settings().AUTH_SALT, max_age=settings().TOKEN_EXPIRATION_TIME)
        except SignatureExpired:
            raise expired_token_exception
        except BadSignature:
            raise no_auth_exception

        outlets = await self._outlet_service.get_all_by_token(token=token)

        if cart_outlet_guid:
            outlet = next((o for o in outlets if o.guid == cart_outlet_guid), None)
            if not outlet:
                raise access_denied_exception
            return outlet

        if price_type_guid:
            if price_type_guid != RETAIL_PRICE_TYPE and not any(
                outlet.price_type_guid == price_type_guid for outlet in outlets
            ):
                raise access_denied_exception
            return None

        return outlets


def get_auth_service(
    outlet_repository: OutletRedisRepository = Depends(),
    outlet_service: OutletService = Depends(),
) -> AuthService:
    return AuthService(outlet_repository=outlet_repository, outlet_service=outlet_service)


async def verify_token(
    token: str = Cookie(None, include_in_schema=False),
    auth_service: AuthService = Depends(get_auth_service),
    cart_outlet_guid: str | None = None,
    price_type_guid: str | None = None,
) -> list[OutletSchema] | OutletSchema | None:
    """
    Универсальная зависимость для проверки токена с дополнительными параметрами.
    """
    return await auth_service.verify_token(
        token=token, cart_outlet_guid=cart_outlet_guid, price_type_guid=price_type_guid
    )
