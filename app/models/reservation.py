from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Reservation(Base):

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    guest_id = Column(
        Integer,
        ForeignKey("guests.id", ondelete="CASCADE"),
        nullable=False
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False
    )

    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    total_price = Column(Float, nullable=False)

    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")