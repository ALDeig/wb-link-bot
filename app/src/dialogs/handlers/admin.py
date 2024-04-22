from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.admin.admin import (
    get_amount_users,
    mailing,
    update_service_message,
)
from app.src.services.admin.texts import (
    CMD_MAILING,
    CMD_SET_CAPTION_TEXT,
    CMD_SET_START_TEXT,
    MAILING_END,
    MAILING_START,
)

router = Router()


# Установка текста для команды старт
@router.message(Command("set_start_text"))
async def cmd_set_start_text(msg: Message, state: FSMContext):
    await msg.answer(CMD_SET_START_TEXT)
    await state.set_state("get_start_text")


@router.message(StateFilter("get_start_text"), flags={"db": True})
async def get_start_text(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    text = await update_service_message(db, "start", msg.html_text)
    await msg.answer(text)


# Установка текста для подписи
@router.message(Command("set_caption_text"))
async def cmd_set_caption_text(msg: Message, state: FSMContext):
    await msg.answer(CMD_SET_CAPTION_TEXT)
    await state.set_state("get_caption_text")


@router.message(StateFilter("get_caption_text"), flags={"db": True})
async def get_caption_text(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    text = await update_service_message(db, "caption", msg.html_text)
    await msg.answer(text)


# Рассылка пользователям
@router.message(Command("mailing"))
async def cmd_mailing(msg: Message, state: FSMContext):
    await msg.answer(CMD_MAILING)
    await state.set_state("get_mailing_message")


@router.message(StateFilter("get_mailing_message"), flags={"db": True})
async def get_mailing_message(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    await msg.answer(MAILING_START)
    await mailing(db, msg)
    await msg.answer(MAILING_END)


# Количество пользователей
@router.message(Command("user_amount"), flags={"db": True})
async def cmd_user_amount(msg: Message, db: AsyncSession):
    text = await get_amount_users(db)
    await msg.answer(text)
