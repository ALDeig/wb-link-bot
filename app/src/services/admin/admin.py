import asyncio

from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
)
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.admin.texts import AMOUNT_USERS, READY
from app.src.services.db.dao.service_message_dao import ServiceMessageDao
from app.src.services.db.dao.user_dao import UserDao


async def update_service_message(session: AsyncSession, title: str, text: str) -> str:
    """Обновление сервисного сообщения"""
    await ServiceMessageDao(session).insert_or_update(title, text)
    return READY


# Рассылка пользователям
async def mailing(session: AsyncSession, msg: Message):
    users = await UserDao(session).find_all()
    for user in users:
        result = await _try_send(msg, user.id)
        if not result:
            await UserDao(session).delete(id=user.id)


async def _try_send(msg: Message, user_id: int) -> bool:
    try:
        await msg.copy_to(user_id)
    except (
        TelegramBadRequest,
        TelegramForbiddenError,
        TelegramUnauthorizedError,
        TelegramNotFound,
    ):
        return False
    except TelegramRetryAfter as er:
        await asyncio.sleep(er.retry_after)
        await _try_send(msg, user_id)
    return True


# Количество пользователей
async def get_amount_users(session: AsyncSession) -> str:
    amount = await UserDao(session).count()
    return AMOUNT_USERS.format(amount=amount)
