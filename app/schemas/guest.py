from pydantic import BaseModel, EmailStr, field_validator

class GuestCreate(BaseModel):

    name: str
    email: EmailStr
    phone: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def phone_format(cls, value: str | None) -> str | None:
        if value is not None and len(value.strip()) < 10:
            raise ValueError("El teléfono debe tener al menos 10 caracteres")
        return value

class GuestResponse(BaseModel):

    id: int
    name: str
    email: str
    phone: str | None

    class Config:
        from_attributes = True