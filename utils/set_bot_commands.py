from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("upcoming", "Eng yaqin tug'ilgan kun"),
            types.BotCommand("all", "Barcha tug'ilgan kunlar"),
            types.BotCommand("me", "Mening ma'lumotlarim"),
            types.BotCommand("register", "Ro'yxatdan o'tish"),
            types.BotCommand("unregister", "Ro'yxatdan o'chish"),
        ]
    )
