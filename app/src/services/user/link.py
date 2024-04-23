import re
from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.user import kb_user_menu
from app.src.services.db.dao.service_message_dao import ServiceMessageDao


@dataclass(slots=True)
class LinkData:
    wb_link: str
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_term: str | None = None
    utm_content: str | None = None


async def get_link(
    session: AsyncSession, data: LinkData
) -> tuple[str, InlineKeyboardMarkup]:
    try:
        link = _create_link(data)
    except NotValideteUrl:
        return "Введена не верная ссылка на товар", kb_user_menu()
    caption = await _get_caption(session)
    return f"{link}\n\n{caption}", kb_user_menu()


def _create_link(data: LinkData) -> str:
    clear_link = data.wb_link.split("?", maxsplit=1)[0]
    scu = _get_article(clear_link)
    link = (
        f"{clear_link}?"
        f"utm_source={data.utm_source}&"
        f"utm_medium={data.utm_medium}&"
        f"utm_campaign={scu}-id-{data.utm_campaign}"
        f"{'&utm_term=' + data.utm_term if data.utm_term else ''}"
        f"{'&utm_content=' + data.utm_content if data.utm_content else ''}"
    )
    link = link.replace(" ", "+")
    return link


async def _get_caption(session: AsyncSession) -> str:
    caption = await ServiceMessageDao(session).find_one_or_none(title="caption")
    if caption is None:
        return "Подпись"
    return caption.text


def _get_article(url: str) -> int:
    """Если передается артикул, то он и возвращается типом int, если url, то
    достается артикул и приводится к int"""
    url_without_params = url.split("?")[0]
    digits = re.search(r"\d+", url_without_params)
    if digits is None:
        raise NotValideteUrl
    return int(digits.group())


class NotValideteUrl(Exception):
    pass
