"""
Здесь храниться код, ответственный за подключение к базе данных:
"""
# Все классы и функции для асинхронной работы
# находятся в модуле sqlalchemy.ext.asyncio.
# Добавляем импорт классов для определения столбца ID.
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)
# Для создания асинхронного движка в SQLAlchemy используется функция create_async_engine()
engine = create_async_engine(settings.database_url)
# Чтобы множественно создавать сессии — примените функцию sessionmaker() из модуля sqlalchemy.orm
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Асинхронный генератор сессий"""
    # Через асинхронный контекстный менеджер и sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
