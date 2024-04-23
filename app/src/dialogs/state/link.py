from aiogram.fsm.state import State, StatesGroup


class LinkState(StatesGroup):
    get_wb_link = State()
    get_utm_source = State()
    get_utm_medium = State()
    get_utm_campaign = State()
    get_utm_term = State()
    get_utm_content = State()
