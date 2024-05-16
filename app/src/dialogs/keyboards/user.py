from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def kb_user_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Создать UTM метку для WB", callback_data="create_link"
                )
            ]
        ]
    )


def kb_utm_source() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="telegram"),
            KeyboardButton(text="vk"),
            KeyboardButton(text="OK"),
        ],
        [
            KeyboardButton(text="seo"),
            KeyboardButton(text="site"),
            KeyboardButton(text="РСЯ"),
        ],
        [
            KeyboardButton(text="YandexDirect"),
            KeyboardButton(text="MyTarget"),
            KeyboardButton(text="YouTube"),
        ],
        [
            KeyboardButton(text="Viber"),
            KeyboardButton(text="WhatsApp"),
            KeyboardButton(text="Instagram"),
        ],
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb


def kb_utm_medium() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="cpc"),
            KeyboardButton(text="email"),
            KeyboardButton(text="storyreels"),
        ],
        [
            KeyboardButton(text="search"),
            KeyboardButton(text="cpm"),
            KeyboardButton(text="retargeting"),
        ],
        [
            KeyboardButton(text="social"),
            KeyboardButton(text="cpa"),
            KeyboardButton(text="banner"),
        ],
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb


def kb_skip():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")]])
