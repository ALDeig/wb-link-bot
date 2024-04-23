from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.user import kb_skip, kb_utm_medium, kb_utm_source
from app.src.dialogs.state.link import LinkState
from app.src.services.user import texts
from app.src.services.user.link import LinkData, get_link
from app.src.services.user.user import cmd_user_start

router = Router()


@router.message(Command("start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    text, kb = await cmd_user_start(
        db, msg.chat.id, msg.chat.full_name, msg.chat.username
    )
    await msg.answer(text, reply_markup=kb, disable_web_page_preview=True)


@router.callback_query(F.data == "create_link", F.message.as_("msg"))
async def btn_create_link(call: CallbackQuery, msg: Message, state: FSMContext):
    await call.answer()
    await msg.answer(texts.GET_WB_LINK, disable_web_page_preview=True)
    await state.set_state(LinkState.get_wb_link)


@router.message(StateFilter(LinkState.get_wb_link))
async def get_wb_link(msg: Message, state: FSMContext):
    await state.update_data(wb_link=msg.text)
    await msg.answer(texts.GET_UTM_SOURCE, reply_markup=kb_utm_source())
    await state.set_state(LinkState.get_utm_source)


@router.message(StateFilter(LinkState.get_utm_source))
async def get_utm_source(msg: Message, state: FSMContext):
    await state.update_data(utm_source=msg.text)
    await msg.answer(texts.GET_UTM_MEDIUM, reply_markup=kb_utm_medium())
    await state.set_state(LinkState.get_utm_medium)


@router.message(StateFilter(LinkState.get_utm_medium))
async def get_utm_medium(msg: Message, state: FSMContext):
    await state.update_data(utm_medium=msg.text)
    await msg.answer(texts.GET_UTM_CAMPAIGN, reply_markup=ReplyKeyboardRemove())
    await state.set_state(LinkState.get_utm_campaign)


@router.message(StateFilter(LinkState.get_utm_campaign))
async def get_utm_campaign(msg: Message, state: FSMContext):
    await state.update_data(utm_campaign=msg.text)
    await msg.answer(texts.GET_UTM_TERM, reply_markup=kb_skip())
    await state.set_state(LinkState.get_utm_term)


@router.message(StateFilter(LinkState.get_utm_term))
async def get_utm_term(msg: Message, state: FSMContext):
    if msg.text != "Пропустить":
        await state.update_data(utm_term=msg.text)
    await msg.answer(texts.GET_UTM_CONTENT, reply_markup=kb_skip())
    await state.set_state(LinkState.get_utm_content)


@router.message(StateFilter(LinkState.get_utm_content), flags={"db": True})
async def get_utm_content(msg: Message, db: AsyncSession, state: FSMContext):
    data = await state.get_data()
    await msg.answer("Ссылка формируется", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    if msg.text != "Пропустить":
        data["utm_content"] = msg.text
    data = LinkData(**data)
    text, kb = await get_link(db, data)
    await msg.answer(text, reply_markup=kb, disable_web_page_preview=True)
