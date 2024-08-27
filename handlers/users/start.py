from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default import user_markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    tg_id = message.from_user.id
    user = db.select_user(tg_id=tg_id)
    if user:
        await message.answer(f"Salom, {message.from_user.full_name}!")
    else:
        await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=user_markup)
