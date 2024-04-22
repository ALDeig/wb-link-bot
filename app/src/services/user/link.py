import re
from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.user import kb_user_menu
from app.src.services.db.dao.service_message_dao import ServiceMessageDao


@dataclass(slots=True)
class LinkData:
    wb_link: str
    product_name: str
    source_name: str
    traffic_type: str


async def create_link(
    session: AsyncSession, data: LinkData
) -> tuple[str, InlineKeyboardMarkup]:
    clear_link = data.wb_link.split("?", maxsplit=1)[0]
    try:
        scu = _get_article(clear_link)
    except NotValideteUrl:
        return "Введена не верная ссылка на товар", kb_user_menu()
    caption = await _get_caption(session)
    link = (
        f"{clear_link}?"
        f"utm_source={data.source_name}&"
        f"utm_medium={data.traffic_type}&"
        f"utm_campaign={scu}-id-{data.product_name}"
        f"\n\n{caption}"
    )
    return link, kb_user_menu()


"""
https://www.wildberries.ru/catalog/158969750/detail.aspx?utm_source=vk&utm_medium=email&utm_campaign=158969750-id-название
"""


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
