"""
Параметр prefix в приведённом коде указывает префикс пути для маршрутизатора, 
в данном случае это '/meeting_rooms'. Все маршруты, определённые в этом роутере, 
будут автоматически иметь префикс с указанным значением, что облегчает управление 
связанными конечными точками.

Параметр tags отвечает за список тегов, которые будут применены ко всем операциям 
пути в этом маршрутизаторе, для группировки в документации.
"""

from fastapi import APIRouter

from app.api.endpoints import (
    google_api_router, meeting_room_router, reservation_router, user_router
)

main_router = APIRouter()
main_router.include_router(
    meeting_room_router, prefix='/meeting_rooms', tags=['Meeting Rooms']
)
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)
main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
main_router.include_router(user_router)
