from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.user import kb_source_name, kb_traffic_type
from app.src.services.user import texts
from app.src.services.user.link import LinkData, create_link
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
    await state.set_state("get_wb_link")


@router.message(StateFilter("get_wb_link"))
async def get_wb_link(msg: Message, state: FSMContext):
    await state.update_data(wb_link=msg.text)
    await msg.answer(texts.GET_PRODUCT_NAME)
    await state.set_state("get_product_name")


@router.message(StateFilter("get_product_name"))
async def get_product_name(msg: Message, state: FSMContext):
    await state.update_data(product_name=msg.text)
    kb = kb_source_name()
    await msg.answer(texts.GET_SOURCE_NAME, reply_markup=kb)
    await state.set_state("get_source_name")


@router.message(StateFilter("get_source_name"))
async def get_source_name(msg: Message, state: FSMContext):
    await state.update_data(source_name=msg.text)
    await msg.answer(texts.GET_TRAFFIC_TYPE, reply_markup=kb_traffic_type())
    await state.set_state("get_traffic_type")


@router.message(StateFilter("get_traffic_type"), flags={"db": True})
async def get_traffic_type(msg: Message, db: AsyncSession, state: FSMContext):
    await msg.answer("Ссылка формируется", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await state.clear()
    data["traffic_type"] = msg.text
    data = LinkData(**data)
    text, kb = await create_link(db, data)
    await msg.answer(text, reply_markup=kb, disable_web_page_preview=True)
