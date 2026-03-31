from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Guest(Base):

    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    phone = Column(String(20), nullable=True)

    reservations = relationship(
        "Reservation",
        back_populates="guest",
        cascade="all, delete-orphan"
    )