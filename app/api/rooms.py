from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.room import RoomCreate, RoomResponse
from app.services import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva habitación"
)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db, data)

@router.get(
    "/",
    response_model=list[RoomResponse],
    summary="Listar todas las habitaciones"
)
def get_rooms(db: Session = Depends(get_db)):
    """Retorna todas las habitaciones registradas en el hotel."""
    return room_service.get_all_rooms(db)

@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Obtener una habitación por ID"
)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.get_room_by_id(db, room_id)

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar una habitación"
)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.delete_room(db, room_id)