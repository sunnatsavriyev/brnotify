import logging

from aiogram import Dispatcher

from data.config import ADMIN


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN, "Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)


async def on_user_register_notify(dp: Dispatcher, user):
    try:
        await dp.bot.send_message(ADMIN, f"{user[1]} {user[2]} bazaga qo'shildi")

    except Exception as err:
        logging.exception(err)
