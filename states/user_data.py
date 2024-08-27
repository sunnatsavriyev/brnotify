from aiogram.dispatcher.filters.state import StatesGroup, State


class UserData(StatesGroup):
    first_name = State()
    last_name = State()
    birth_date = State()
    confirm = State()
