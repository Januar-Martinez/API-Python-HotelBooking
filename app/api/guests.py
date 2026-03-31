from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.guest import GuestCreate, GuestResponse
from app.services import guest_service

router = APIRouter(prefix="/guests", tags=["Guests"])

@router.post(
    "/",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo huésped"
)
def create_guest(
    data: GuestCreate,
    db: Session = Depends(get_db)
):
    return guest_service.create_guest(db, data)

@router.get(
    "/",
    response_model=list[GuestResponse],
    summary="Listar todos los huéspedes"
)
def get_guests(db: Session = Depends(get_db)):
    """Retorna la lista completa de huéspedes registrados."""
    return guest_service.get_all_guests(db)

@router.get(
    "/{guest_id}",
    response_model=GuestResponse,
    summary="Obtener un huésped por ID"
)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    return guest_service.get_guest_by_id(db, guest_id)


@router.delete(
    "/{guest_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un huésped"
)
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    return guest_service.delete_guest(db, guest_id)