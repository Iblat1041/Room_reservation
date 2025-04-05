from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Для работы с переменными окружениями в FastAPI , 
    унаследованный от класса BaseSettings 
    """
    app_title: str = 'Бронирование переговорок'
    database_url: str
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
