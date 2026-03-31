from datetime import date
from pydantic import BaseModel, field_validator, model_validator

class ReservationCreate(BaseModel):

    guest_id: int
    room_id: int
    check_in: date    # Formato: "YYYY-MM-DD"
    check_out: date

    @field_validator("check_in")
    @classmethod
    def check_in_not_in_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("La fecha de check_in no puede ser en el pasado")
        return value

    @model_validator(mode="after")
    def check_out_after_check_in(self) -> "ReservationCreate":
        if self.check_out <= self.check_in:
            raise ValueError("check_out debe ser posterior a check_in")
        return self

class ReservationResponse(BaseModel):

    id: int
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    total_price: float

    class Config:
        from_attributes = True

class RoomOccupancy(BaseModel):
    room_id: int
    room_number: str
    total_reservations: int
    total_nights: int
    total_revenue: float


class StatisticsResponse(BaseModel):
    total_revenue: float
    total_reservations: int
    occupancy_by_room: list[RoomOccupancy]
    most_booked_room: str | None