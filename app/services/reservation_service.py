from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.reservation import Reservation
from app.models.room import Room
from app.models.guest import Guest
from app.schemas.reservation import ReservationCreate

def _check_date_overlap(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_reservation_id: int | None = None
) -> bool:
    query = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.check_in < check_out,
        Reservation.check_out > check_in
    )

    if exclude_reservation_id:
        query = query.filter(Reservation.id != exclude_reservation_id)

    return query.first() is not None

def _calculate_total_price(room: Room, check_in: date, check_out: date) -> float:
    nights = (check_out - check_in).days
    return nights * room.price

def create_reservation(db: Session, data: ReservationCreate) -> Reservation:
    guest = db.query(Guest).filter(Guest.id == data.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Huésped con id {data.guest_id} no encontrado"
        )

    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habitación con id {data.room_id} no encontrada"
        )

    if not room.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La habitación '{room.number}' no está disponible"
        )

    if _check_date_overlap(db, data.room_id, data.check_in, data.check_out):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"La habitación '{room.number}' ya tiene una reserva "
                f"que se superpone con las fechas {data.check_in} → {data.check_out}"
            )
        )

    total_price = _calculate_total_price(room, data.check_in, data.check_out)

    reservation = Reservation(
        guest_id=data.guest_id,
        room_id=data.room_id,
        check_in=data.check_in,
        check_out=data.check_out,
        total_price=total_price
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def get_all_reservations(db: Session) -> list[Reservation]:
    """Retorna todas las reservas registradas."""
    return db.query(Reservation).all()

def get_reservation_by_id(db: Session, reservation_id: int) -> Reservation:
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con id {reservation_id} no encontrada"
        )
    return reservation

def delete_reservation(db: Session, reservation_id: int) -> dict:
    reservation = get_reservation_by_id(db, reservation_id)
    db.delete(reservation)
    db.commit()
    return {"message": f"Reserva con id {reservation_id} eliminada correctamente"}