from typing import Optional

# Добавляем к списку импортов импорт jsonable_encoder.
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select

# Импортируем класс асинхронной сессии для аннотаций.
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


# Функция работает с асинхронной сессией AsyncSession,
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession,
) -> MeetingRoom:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_room_data = new_room.dict()

    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    db_room = MeetingRoom(**new_room_data)

    # Добавляем созданный объект в сессию.
    # Никакие действия с базой пока ещё не выполняются.
    session.add(db_room)
    # Записываем изменения непосредственно в БД.
    # Так как сессия асинхронная, используем ключевое слово await.
    await session.commit()
    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room


async def get_room_id_by_name(
        room_name: str,
        # Добавляем новый параметр.
        session: AsyncSession,
) -> Optional[int]:
    # Убираем контекстный менеджер.
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def read_all_rooms_from_db(
        session: AsyncSession,
) -> list[MeetingRoom]:
    db_rooms = await session.execute(select(MeetingRoom))
    return db_rooms.scalars().all() 


async def get_meeting_room_by_id(
        room_id: int,
        session: AsyncSession,
) -> Optional[MeetingRoom]:
    """Функция для получения объекта по его ID """
    db_room = await session.execute(
        select(MeetingRoom).where(
            MeetingRoom.id == room_id
        )
    )
    db_room = db_room.scalars().first()
    return db_room 


async def update_meeting_room(
        # Объект из БД для обновления.
        db_room: MeetingRoom,
        # Объект из запроса.
        room_in: MeetingRoomUpdate,
        session: AsyncSession,
) -> MeetingRoom:
    """Функция для обновления объекта."""
    # Получаем из БД объект с помощью jsonable_encoder()
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запроса в словарь, 
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True)

    # Перебираем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
            # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
    # Добавляем обновленный объект в сессию.
    session.add(db_room)
    # Фиксируем изменения.
    await session.commit() 
    # Обновляем объект из БД.
    await session.refresh(db_room)
    return db_room


async def delete_meeting_room(
        db_room: MeetingRoom,
        session: AsyncSession,
) -> MeetingRoom:
    # Удаляем объект из БД.
    await session.delete(db_room)
    # Фиксируем изменения в БД.
    await session.commit()
    # Не обновляем объект через метод refresh(), 
    # следовательно он всё ещё содержит информацию об удаляемом объекте.
    return db_room 


