from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.guest import Guest
from app.schemas.guest import GuestCreate

def create_guest(db: Session, data: GuestCreate) -> Guest:
    existing = db.query(Guest).filter(Guest.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un huésped registrado con el email '{data.email}'"
        )

    guest = Guest(
        name=data.name,
        email=data.email,
        phone=data.phone
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

def get_all_guests(db: Session) -> list[Guest]:
    return db.query(Guest).all()

def get_guest_by_id(db: Session, guest_id: int) -> Guest:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Huésped con id {guest_id} no encontrado"
        )
    return guest

def delete_guest(db: Session, guest_id: int) -> dict:
    guest = get_guest_by_id(db, guest_id)
    db.delete(guest)
    db.commit()
    return {"message": f"Huésped '{guest.name}' eliminado correctamente"}