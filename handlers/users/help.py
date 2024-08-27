from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
            "Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/upcoming - Kelayotgan tug'ilgan kun",
            "/all - Barcha tug'ilgan kunlar",
            "/me - Foydalanuvchi haqida ma'lumotlar",
            "/register - Ro'yxatdan o'tish",
            "/unregister - Ro'yxatdan o'chish",
        )

    await message.answer("\n".join(text))
