import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db


@dp.message_handler(Command('upcoming'))
async def upcoming_birthday(message: types.Message):
    current_day_number = int(datetime.date.today().strftime('%j'))
    days_in_year = 365

    users = db.select_all_users()
    upcoming_br_days = []
    for user in users:
        user_birthday = user[4]
        current_year = datetime.datetime.now().year
        date_part, time_part = user_birthday.split(" ", 1)
        _, month_day = date_part.split("-", 1)
        user_birthday_with_year = f"{current_year}-{month_day} {time_part}"
        user_birthday_number = int(datetime.datetime.strptime(user_birthday_with_year, "%Y-%m-%d %H:%M:%S").strftime('%j'))
        days_until_br_day = user_birthday_number - current_day_number
        if days_until_br_day < 0:
            days_until_br_day = days_in_year - current_day_number + user_birthday_number
        if days_until_br_day != 0:
            upcoming_br_days.append((user, days_until_br_day))
    upcoming_br_days.sort(key=lambda row: row[1])
    upcoming_br_day_user = upcoming_br_days[0][0]
    upcoming_br_day_user_br_day = datetime.datetime.strptime(upcoming_br_day_user[4], "%Y-%m-%d %H:%M:%S").strftime("%B %d")
    message_text = f"Keyingi tug'ilgan kunga {upcoming_br_days[0][1]} kun qoldi\n\n"
    message_text += f"<b>{upcoming_br_day_user[1]} {upcoming_br_day_user[2]}</b>\n"
    message_text += f"{upcoming_br_day_user_br_day}"
    await message.answer(message_text)


@dp.message_handler(Command('all'))
async def show_all_birthdays(message: types.Message):
    users = db.select_all_users()
    birthdays = {}
    for month in range(1, 13):
        month_name = datetime.date(month=month, year=1, day=1).strftime('%B')
        birthdays[f'{month_name}'] = []
        for user in users:
            if datetime.datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S").month == month:
                user_br_day = datetime.datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S").day
                birthdays[f'{month_name}'].append((user, user_br_day))
    message_text = ''
    for item in birthdays:
        if birthdays[item]:
            birthdays[item].sort(key=lambda row: row[1])
            message_text += f'<b>{item}</b>\n\n'
            for index, user_data in enumerate(birthdays[item]):
                user_birth_day = datetime.datetime.strptime(user_data[0][4], "%Y-%m-%d %H:%M:%S").strftime('%B %d')
                message_text += f'{index+1}. {user_data[0][1]} {user_data[0][2]} - {user_birth_day}\n'
            message_text += 30 * '_'
            message_text += '\n\n'

    await message.answer(message_text)
