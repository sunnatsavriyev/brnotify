from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.notify_users import notify_user, notify_br_day_user


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)






if __name__ == '__main__':

    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_user, 'cron', hour=9, minute=00)
    scheduler.add_job(notify_br_day_user, 'cron', hour=9, minute=08)
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    
