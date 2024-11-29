from schemas.base import BaseOrmSchema


class ContactMeCreateSchema(BaseOrmSchema):
    full_name: str
    is_company: bool
    email: str | None
    phone: str | None
