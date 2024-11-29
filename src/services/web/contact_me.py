import aiohttp

from core.config import settings
from core.exceptions import (
    incorrect_contact_me_form_exception,
)
from schemas.contact_me import ContactMeCreateSchema


class ContactMeService:
    @staticmethod
    async def create(data: ContactMeCreateSchema) -> ContactMeCreateSchema:
        if not data.email and not data.phone:
            raise incorrect_contact_me_form_exception

        async with aiohttp.ClientSession() as session:
            async with session.post(settings().contact_me_1c_url, json=data.model_dump()) as response:
                print(await response.text())
                # if response.status != status.HTTP_200_OK:
                #     logger.error(
                #         f"{contact_me_form_exception.detail} Ошибка: {response.status} | {await response.json()}"
                #     )
                #     raise contact_me_form_exception

        return data
