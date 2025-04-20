from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class IncomingMessage(BaseModel):
    # Модифицируйте атрибуты, чтобы они соответствовали заданию.
    title: Optional[str] = Field(default='У этого сообщения нет заголовка')
    body: str
    contacts: Optional[str]
    secret_hash: str


class OutgoingMessage(BaseModel):
    title: Optional[str]
    body: str
    contacts: Optional[str]


# Модифицируйте эндпоинт так,
# чтобы он выполнял поставленную задачу.
@app.post(
    '/post-office',
    response_model=OutgoingMessage,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True
)
def sloth(message: IncomingMessage):
    # Отсюда можно передать данные для обработки и сохранения в БД,
    # но этого писать мы не будем. И вам не нужно.
    return message