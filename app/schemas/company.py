from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    description: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_visible: bool | None = None

class CompanySchema(BaseModel):
    id: int
    name: str
    description: str | None
    is_visible: bool
    owner_id: int

    model_config = {
        "from_attributes": True
    }
