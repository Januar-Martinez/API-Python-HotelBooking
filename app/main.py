from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db import init_db
from app.api import guests, rooms, reservations, statistics

app = FastAPI(
    title=settings.APP_NAME,
    description="""
API RESTful para gestionar reservas de habitaciones en un hotel.

## Funcionalidades
- 🧑 Gestión de **huéspedes**
- 🛏️ Gestión de **habitaciones**
- 📅 Gestión de **reservas** con control de disponibilidad
- 📊 **Estadísticas** de ocupación e ingresos
    """,
    version="1.0.0",
)

init_db()

app.include_router(guests.router)
app.include_router(rooms.router)
app.include_router(statistics.router)
app.include_router(reservations.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación en los datos enviados",
            "errors": exc.errors()
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno en la base de datos. Intenta más tarde."
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor. Intenta más tarde."
        }
    )

@app.get("/", tags=["Root"], summary="Bienvenida y estado de la API")
def root():
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "status": "running",
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "redoc": "/redoc"
    }