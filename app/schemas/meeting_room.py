# Модели в Pydantic — это классы, которые наследуются от класса BaseModel. 
# Они используются для определения структуры данных, проверки и логики синтаксического анализа данных
# Каждая модель описывает набор полей, которые представляют собой данные и условия для их валидации. 

from typing import Optional


from pydantic import BaseModel, Field, validator


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


# Новый класс для обновления объектов.
class MeetingRoomUpdate(MeetingRoomBase):

    #дополнительно валидировать поле name на то, что оно не равно None
    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


# Теперь наследуем схему не от BaseModel, а от MeetingRoomBase.
class MeetingRoomCreate(MeetingRoomBase):
    # Переопределяем атрибут name, делаем его обязательным.
    name: str = Field(..., min_length=1, max_length=100)
    # Описывать поле description не нужно: оно уже есть в базовом классе.


# Возвращаемую схему унаследуем от MeetingRoomCreate, 
# чтобы снова не описывать обязательное поле name.
class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True 