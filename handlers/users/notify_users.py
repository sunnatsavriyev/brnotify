import datetime

from loader import db, dp
from data.config import ADMIN


async def notify_user():
    users = list(db.select_all_users())
    today_day_number = int(datetime.date.today().strftime('%j'))
    tomorrow_day = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow_day_str = tomorrow_day.strftime('%B %d')
    br_day_users = []
    for user in users:
        user_birthday = user[4]
        current_year = datetime.datetime.now().year
        date_part, time_part = user_birthday.split(" ", 1)
        _, month_day = date_part.split("-", 1)
        user_birthday_with_year = f"{current_year}-{month_day} {time_part}"
        user_birthday_day_number = int(datetime.datetime.strptime(user_birthday_with_year, "%Y-%m-%d %H:%M:%S").strftime('%j'))
        if user_birthday_day_number - today_day_number == 1:
            br_day_users.append(user)
            users.remove(user)
    if br_day_users:
        for user in users:
            message_text = f'Ertaga {tomorrow_day_str}\n'
            for br_day_user in br_day_users:
                message_text += f'<b>{br_day_user[1]} {br_day_user[2]}</b> ning\n'
            message_text += "Tug'ilgan kuni\n"
            message_text += "Jamoa bilan tabriklashni unutmang\n "
            await dp.bot.send_message(chat_id=user[3], text=message_text)


async def notify_br_day_user():
    users = list(db.select_all_users())
    today_day_number = int(datetime.date.today().strftime('%j'))
    br_day_users = []
    for user in users:
        user_birthday = user[4]
        current_year = datetime.datetime.now().year
        date_part, time_part = user_birthday.split(" ", 1)
        _, month_day = date_part.split("-", 1)
        user_birthday_with_year = f"{current_year}-{month_day} {time_part}"
        user_birthday_day_number = int(datetime.datetime.strptime(user_birthday_with_year, "%Y-%m-%d %H:%M:%S").strftime('%j'))
        if user_birthday_day_number - today_day_number == 0:
            br_day_users.append(user)
    if br_day_users:
        for user in br_day_users:
            message_text = f'Hurmatli {user[1]} {user[2]},\n'
            message_text += "Sizni tug'ilgan kuningiz bilan <b>UNICON</b> jamoasi tabriklaydi\n"
            message_text += "Hayotda qo'ygan barcha maqsadlaringizga erishishingizga tilakdoshmiz\n"
            message_text += "Birgalikda yanada ko'p yutuqlarga erishishga ishonamiz\n"
            if user[2].endswith('a'):
                message_text += '🌹🌹🎉🎉🎁🎁🎂🎂'
            else:
                message_text += '🎂🎂🎂🎂🎂🎂🎂🎂'
            await dp.bot.send_message(chat_id=user[3], text=message_text)
            await dp.bot.send_sticker(chat_id=user[3], sticker="CAACAgIAAxkBAAIBAWVpSAY8U81Wj2XO4TdtPquMlxbcAAL-RwACnIVpSOQlOMLuOz-7MwQ")