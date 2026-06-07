from pydantic import BaseModel, ConfigDict


class CSetModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    description: str = ""