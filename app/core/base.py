"""импортируем модели не в Alembic напрямую, а в специальный файл app/core/base.py. 
В этот же файл импортируем класс Base из файла app/core/db.py. 

И будем импортировать класс Base в alembic/env.py не из app/core/db.py, а из app/core/base.py.

Тогда при импорте класса Base интерпретатор заодно увидит все остальные модели, и информация о 
них будет доступна Alembic в Base.metadata. После этого будет достаточно импортировать 
в Alembic только класс Base.
 """

"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base # noqa
from app.models.meeting_room import MeetingRoom  # noqa

