from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services import reservation_service

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reserva"
)
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db)):
    return reservation_service.create_reservation(db, data)

@router.get(
    "/",
    response_model=list[ReservationResponse],
    summary="Listar todas las reservas"
)
def get_reservations(db: Session = Depends(get_db)):
    return reservation_service.get_all_reservations(db)

@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
    summary="Obtener una reserva por ID"
)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return reservation_service.get_reservation_by_id(db, reservation_id)

@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    summary="Cancelar una reserva"
)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return reservation_service.delete_reservation(db, reservation_id)