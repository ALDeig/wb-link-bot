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


def kb_source_name() -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text="telegram"), KeyboardButton(text="vk")]]
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb


def kb_traffic_type() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="cpc"), KeyboardButton(text="email")],
        [KeyboardButton(text="banner"), KeyboardButton(text="article")],
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb
