# 🏨 API Python HotelBooking

API RESTful construida con **FastAPI** y **SQLite** para gestionar reservas
de habitaciones en un hotel. Controla disponibilidad, evita sobre-reservas
y genera estadísticas de ocupación.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.11+ | Lenguaje base |
| FastAPI | Framework web |
| SQLAlchemy | ORM (mapeo objeto-relacional) |
| Pydantic v2 | Validación de datos |
| SQLite | Base de datos |
| Uvicorn | Servidor ASGI |

---

## 🗄️ Modelo de datos
```
guests                reservations              rooms
──────────            ────────────              ─────
id                    id                        id
name                  guest_id (FK)             number
email                 room_id  (FK)             type
phone                 check_in                  price
                      check_out                 is_available
                      total_price
```

---