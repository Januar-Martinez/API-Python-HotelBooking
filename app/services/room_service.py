from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.room import Room
from app.schemas.room import RoomCreate

def create_room(db: Session, data: RoomCreate) -> Room:
    existing = db.query(Room).filter(Room.number == data.number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una habitación con el número '{data.number}'"
        )

    room = Room(
        number=data.number,
        type=data.type.value,
        price=data.price,
        is_available=data.is_available
    )

    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_all_rooms(db: Session) -> list[Room]:
    return db.query(Room).all()

def get_room_by_id(db: Session, room_id: int) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habitación con id {room_id} no encontrada"
        )
    return room

def delete_room(db: Session, room_id: int) -> dict:
    room = get_room_by_id(db, room_id)
    db.delete(room)
    db.commit()
    return {"message": f"Habitación '{room.number}' eliminada correctamente"}