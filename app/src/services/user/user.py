from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.user import kb_user_menu
from app.src.services.db.dao.service_message_dao import ServiceMessageDao
from app.src.services.db.dao.user_dao import UserDao
from app.src.services.user.texts import DEFAULT_START


async def cmd_user_start(
    session: AsyncSession, user_id: int, full_name: str, username: str | None
) -> tuple[str, InlineKeyboardMarkup]:
    await UserDao(session).insert_or_nothing(user_id, full_name, username)
    start_message = await ServiceMessageDao(session).find_one_or_none(title="start")
    kb = kb_user_menu()
    if start_message is None:
        return DEFAULT_START, kb
    return start_message.text, kb
