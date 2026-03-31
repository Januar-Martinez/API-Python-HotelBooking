from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.reservation import Reservation
from app.models.room import Room
from app.schemas.reservation import StatisticsResponse, RoomOccupancy

def get_statistics(db: Session) -> StatisticsResponse:
    total_revenue = db.query(func.sum(Reservation.total_price)).scalar() or 0.0
    total_reservations = db.query(func.count(Reservation.id)).scalar() or 0

    occupancy_data = (
        db.query(
            Room.id.label("room_id"),
            Room.number.label("room_number"),
            func.count(Reservation.id).label("total_reservations"),
            func.sum(
                func.julianday(Reservation.check_out) -
                func.julianday(Reservation.check_in)
            ).label("total_nights"),
            func.sum(Reservation.total_price).label("total_revenue")
        )
        .join(Reservation, Room.id == Reservation.room_id)
        .group_by(Room.id, Room.number)
        .all()
    )

    occupancy_list = [
        RoomOccupancy(
            room_id=row.room_id,
            room_number=row.room_number,
            total_reservations=row.total_reservations,
            total_nights=int(row.total_nights or 0),
            total_revenue=row.total_revenue or 0.0
        )
        for row in occupancy_data
    ]

    most_booked = (
        max(occupancy_list, key=lambda x: x.total_reservations)
        if occupancy_list else None
    )

    return StatisticsResponse(
        total_revenue=total_revenue,
        total_reservations=total_reservations,
        occupancy_by_room=occupancy_list,
        most_booked_room=most_booked.room_number if most_booked else None
    )