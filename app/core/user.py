# app/core/user.py
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

# SQLAlchemyUserDatabase — это функция, которая используется в пакете FastAPI Users для работы с базами данных SQL.  12
async def get_user_db(
        session: AsyncSession = Depends(get_async_session)
        ):
    """
     Aсинхронный генератор, позволяет создавать адаптер для взаимодействия с базой данных, 
     передавая в качестве параметров экземпляр сессии и класс модели пользователя
    """
    yield SQLAlchemyUserDatabase(session, User)

# Определяем транспорт: передавать токен будем
# через заголовок HTTP-запроса Authorization: Bearer.
# Указываем URL эндпоинта для получения токена.
#BearerTransport — это транспорт, при использовании которого токен ожидается в заголовке Authorization HTTP-запроса по схеме Bearer.
bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

# Определяем стратегию: хранение токена в виде JWT.
def get_jwt_strategy() -> JWTStrategy:
    # В специальный класс из настроек приложения
    # передаётся секретное слово, используемое для генерации токена.
    # Вторым аргументом передаём срок действия токена в секундах.
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)

# Создаём объект бэкенда аутентификации с выбранными параметрами.
auth_backend = AuthenticationBackend(
    name='jwt',  # Произвольное имя бэкенда (должно быть уникальным).
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Args:
        IntegerIDMixin : обеспечивает возможность использования
            целочисленных id для таблицы пользователей
        BaseUserManager : этом классе производятся основные действия:
            аутентификация, регистрация, сброс пароля, верификация и другие.
    """

    # Здесь можно описать свои условия валидации пароля.
    # При успешной валидации функция ничего не возвращает.
    # При ошибке валидации будет вызван специальный класс ошибки
    # InvalidPasswordException.
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Метод для действий после успешной регистрации пользователя."""
        # Вместо print здесь можно было бы настроить отправку письма.
        print(f'Пользователь {user.email} зарегистрирован.')



async def get_user_manager(user_db=Depends(get_user_db)):
    """Корутина, возвращающая объект класса UserManager"""
    yield UserManager(user_db)

# Центральный объект библиотеки, связывающий объект класса UserManager
# и бэкенд аутентификации
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Это методы класса FastAPIUsers, которые мы будем использовать в системе
# Dependency Injection для получения текущего пользователя при выполнении
# запросов, а также для разграничения доступа: некоторые эндпоинты будут
# доступны только суперюзерам.
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
