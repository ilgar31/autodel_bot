from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import add_chat_request, assign_admin_to_chat, get_chat_request, end_chat, get_chat_request_for_admin
from config import ADMINS
from keyboards.main_menu import get_main_menu
from aiogram import F

router = Router()

@router.message(F.text == "📝 Написать администратору")  # Фильтруем по тексту сообщения
async def request_chat(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, не начат ли уже диалог
    if get_chat_request(user_id):
        await message.answer("❌ Вы уже в активном диалоге.")
        return

    # Добавляем запрос на диалог
    add_chat_request(user_id)

    # Создаем клавиатуру с кнопкой "Закончить диалог"
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Закончить диалог")]], resize_keyboard=True)
    await message.answer("⏳ Пожалуйста, подождите, пока специалист освободится.", reply_markup=keyboard)

    # Отправляем уведомление всем администраторам
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Принять", callback_data=f"accept_{user_id}")

    for admin_id in ADMINS:
        if not get_chat_request_for_admin(admin_id):
            await message.bot.send_message(
                admin_id,
                f"Пользователь @{message.from_user.username} хочет начать диалог.",
                reply_markup=builder.as_markup()
            )

@router.callback_query(lambda c: c.data.startswith("accept_"))
async def accept_chat_request(call: types.CallbackQuery):
    admin_id = call.from_user.id
    user_id = int(call.data.split("_")[1])

    # Назначаем администратора на диалог
    assign_admin_to_chat(user_id, admin_id)

    # Уведомляем пользователя
    await call.bot.send_message(user_id, "✅ Специалист нашелся! Вы можете начать диалог.")

    # Уведомляем администратора
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Закончить диалог")]], resize_keyboard=True)
    await call.bot.send_message(admin_id, f"✅ Вы начали диалог с пользователем.", reply_markup=keyboard)
    await call.message.delete()


    # Уведомляем остальных администраторов
    for other_admin_id in ADMINS:
        if other_admin_id != admin_id:
            await call.bot.send_message(other_admin_id, f"Диалог с пользователем уже ведет другой администратор.")

@router.message(lambda message: message.text == "❌ Закончить диалог")
async def end_chat_command(message: types.Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        admin_id = get_chat_request_for_admin(user_id)
        user_id, admin_id = admin_id, user_id
        end_chat(user_id)
        await message.bot.send_message(admin_id, "❌ Диалог завершен.",
                                       reply_markup=get_main_menu(admin_id))

        await message.bot.send_message(user_id, "❌ Диалог завершен.")
        await message.bot.send_message(user_id, "Администратор завершил диалог.",
                                       reply_markup=get_main_menu(user_id))

    else:
        admin_id = get_chat_request(user_id)
        end_chat(user_id)
        await message.bot.send_message(admin_id,"❌ Диалог завершен.")
        await message.bot.send_message(admin_id, f"Пользователь @{message.from_user.username} завершил диалог.", reply_markup=get_main_menu(admin_id))

        await message.bot.send_message(user_id,"❌ Диалог завершен.", reply_markup=get_main_menu(user_id))

@router.message()
async def forward_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        admin_id = get_chat_request_for_admin(user_id)
        user_id, admin_id = admin_id, user_id
        await message.bot.send_message(user_id, f"{message.text}")

    else:
        admin_id = get_chat_request(user_id)
        await message.bot.send_message(admin_id, f"Сообщение от пользователя @{message.from_user.username}:\n{message.text}")
