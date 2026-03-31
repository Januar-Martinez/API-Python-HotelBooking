from enum import Enum
from pydantic import BaseModel, field_validator

class RoomType(str, Enum):
    simple = "simple"
    doble = "doble"
    suite = "suite"

class RoomCreate(BaseModel):

    number: str
    type: RoomType
    price: float
    is_available: bool = True

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return value

    @field_validator("number")
    @classmethod
    def number_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El número de habitación no puede estar vacío")
        return value.strip()

class RoomResponse(BaseModel):

    id: int
    number: str
    type: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True