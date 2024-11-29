from pydantic import ConfigDict, BaseModel


class BaseOrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
