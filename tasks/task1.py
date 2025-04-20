from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

app = FastAPI()
Base = declarative_base()


class SecretMessage(BaseModel):
    title: str
    message: str


class ReadyNews(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)


def decoder(data: dict[str, str]) -> dict[str, str]:
    """
    Сверхсекретный декодер.

    Здесь всё работает, ничего менять не надо!
    """
    decoded_data = {}
    for key, value in data.items():
        decoded_str = (chr(int(chunk)) for chunk in value.split('-'))
        decoded_data[key] = ''.join(decoded_str)
    return decoded_data


@app.post('/super-secret-base')
def reciever(encoded_news: SecretMessage):

    # Передайте сообщение в декодер.
    ready_news = ReadyNews(**decoder(encoded_news.dict()))

    # Создайте переменную ready_news - объект класса ReadyNews
    # из дешифрованного сообщения.

    # Здесь мог бы быть код, сохраняющий сообщение в базу данных,
    # но его писать не надо.

    # Эндпоинт возвращает объект класса ReadyNews.
    # Здесь ничего менять не надо.
    return ready_news
