import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, db
from states.user_data import UserData
from keyboards.default import user_data_confirm, user_markup
from utils.notify_admins import on_user_register_notify
from data.config import ADMIN


@dp.message_handler(text="Ro'yxatdan o'tish")
@dp.message_handler(Command("register"))
async def user_register(message: types.Message):
    tg_id = message.from_user.id
    user = db.select_user(tg_id=tg_id)
    if user:
        await message.answer("Siz ro'yxatdan o'tgansiz")
    else:
        await message.answer('Ismingizni kiriting', reply_markup=types.ReplyKeyboardRemove())
        await UserData.first_name.set()


@dp.message_handler(Command("unregister"))
async def user_unregister(message: types.Message):
    tg_id = message.from_user.id
    user = db.select_user(tg_id=tg_id)
    if user:
        db.delete_user(tg_id=tg_id)
        await message.answer("Siz ro'yxatdan o'chirildingiz", reply_markup=user_markup)
        await dp.bot.send_message(ADMIN, f"{user[1]} {user[2]} bazadan o'chirildi")
    else:
        await message.answer("Siz ro'yxatdan o'tmagansiz", reply_markup=user_markup)



@dp.message_handler(Command("unregister"))
async def user_unregister(message: types.Message):
    tg_id = message.from_user.id
    
    if tg_id == ADMIN:
        # Admin wants to delete a user by their first and last name
        await message.answer("O'chirilishi kerak bo'lgan foydalanuvchining ismi va familyasini yuboring (masalan, John Doe):")
        
        @dp.message_handler()
        async def get_user_name(msg: types.Message):
            name_parts = msg.text.split()
            if len(name_parts) != 2:
                await msg.answer("Iltimos, foydalanuvchining to'liq ismi va familyasini kiriting.")
                return
            
            first_name, last_name = name_parts
            user = db.select_user_by_name(first_name=first_name, last_name=last_name)
            
            if user:
                db.delete_user(tg_id=user['tg_id'])
                await msg.answer(f"Foydalanuvchi {user['first_name']} {user['last_name']} bazadan o'chirildi", reply_markup=user_markup)
            else:
                await msg.answer("Foydalanuvchi topilmadi", reply_markup=user_markup)

@dp.message_handler(Command('me'))
async def about_me(message: types.Message):
    tg_id = message.from_user.id
    user = db.select_user(tg_id=tg_id)
    if user:
        birthday = user[4]
        str_birth_date = datetime.datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S").strftime('%B %d')
        message_text = f"Ism: {user[1]}\n"
        message_text += f"Familiya: {user[2]}\n"
        message_text += f"Tug'ilgan kuningiz: {str_birth_date}"
        await message.answer(message_text, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Siz ro'yxatdan o'tmagansiz", reply_markup=user_markup)


@dp.message_handler(state=UserData.first_name)
async def answer_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    tg_id = message.from_user.id
    await state.update_data({'first_name': first_name, 'tg_id': tg_id})
    await message.answer('Familiyangizni kiriting')
    await UserData.next()


@dp.message_handler(state=UserData.last_name)
async def answer_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data({'last_name': last_name})
    await message.answer("Tug'ilgan oy va kuningizni kiriting\nMisol uchun: 31.12 ko'rinishida")
    await UserData.next()


@dp.message_handler(state=UserData.birth_date)
async def answer_birth_date(message: types.Message, state: FSMContext):
    try:
        month, day = message.text.split('.')
        birth_date = datetime.datetime.strptime(f'{month}-{day}', '%d-%m')
    except ValueError:
        await message.answer("Tug'ilgan kuningizni no'tog'ri formatda kiritdingiz\n"
                             "Iltimos 31.12 ko'rinishida kiriting")
    else:
        await state.update_data({'birth_date': birth_date})

        user_data = await state.get_data()
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        birthday = user_data.get('birth_date')
        str_birth_date = birthday.strftime("%B %d")
        message_text = "Ma'lumotlarni tasdiqlang\n"
        message_text += f"Ism:   {first_name}\n"
        message_text += f"Familiya:   {last_name}\n"
        message_text += f"Tug'ilgan kuningiz:   {str_birth_date}"
        await message.answer(message_text, reply_markup=user_data_confirm)
        await UserData.next()


@dp.message_handler(state=UserData.confirm, text="Tasdiqlash")
async def answer_user_data_confirm(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    birthday = user_data.get('birth_date')
    tg_id = user_data.get('tg_id')
    db.add_user(first_name=first_name, last_name=last_name, tg_id=tg_id, birthday=birthday)
    user = db.select_user(tg_id=tg_id)
    message_text = "Siz ro'yxatdan muvaffaqiyatli o'tdingiz\n"
    await message.answer(message_text, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await on_user_register_notify(dp=dp, user=user)


@dp.message_handler(state=UserData.confirm, text="Bekor qilish")
async def answer_user_data_confirm(message: types.Message, state: FSMContext):
    await message.answer("Ma'lumotlar bekor qilindi", reply_markup=user_markup)
    await state.finish()
