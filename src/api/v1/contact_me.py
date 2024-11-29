from fastapi import APIRouter, status, Depends

from schemas.contact_me import ContactMeCreateSchema
from services.web.contact_me import ContactMeService

router = APIRouter(prefix="/contact-me", tags=["Форма 'Свяжитесь с нами'"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ContactMeCreateSchema,
)
async def create_contact_me_form(
    data: ContactMeCreateSchema,
    contact_me_service: ContactMeService = Depends(),
) -> ContactMeCreateSchema:
    return await contact_me_service.create(data=data)
