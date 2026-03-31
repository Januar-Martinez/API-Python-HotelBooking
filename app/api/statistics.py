from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.reservation import StatisticsResponse
from app.services import statistics_service

router = APIRouter(prefix="/reservations", tags=["Statistics"])

@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    summary="Estadísticas de ocupación e ingresos"
)
def get_statistics(db: Session = Depends(get_db)):
    return statistics_service.get_statistics(db)