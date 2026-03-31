from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    number = Column(String(10), unique=True, nullable=False, index=True)

    type = Column(String(20), nullable=False)

    price = Column(Float, nullable=False)

    is_available = Column(Boolean, default=True, nullable=False)

    reservations = relationship(
        "Reservation",
        back_populates="room",
        cascade="all, delete-orphan"
    )