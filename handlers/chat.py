from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import add_chat_request, assign_admin_to_chat, save_non_working_hours_request, get_chat_request, end_chat, get_chat_request_for_admin, add_admin_notification, get_admin_notifications, delete_admin_notifications
from config import ADMINS
from keyboards.main_menu import get_main_menu
from aiogram import F
from datetime import datetime, time

router = Router()


# Определяем рабочее время (с 8:00 до 19:00)
WORK_START = time(8, 0)  # 8:00
WORK_END = time(19, 0)   # 19:00

def is_working_hours():
    now = datetime.now().time()
    return WORK_START <= now <= WORK_END

@router.message(F.text == "📝 Написать администратору")
async def request_chat(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, не начат ли уже диалог
    if get_chat_request(user_id):
        await message.answer("❌ Вы уже в активном диалоге.")
        return

    # Проверяем, рабочее ли время
    if not is_working_hours():
        await message.answer(
            "Добрый вечер, дорогой клиент! Наши администраторы обязательно ответят вам в рабочее время.")

        # Записываем запрос пользователя в базу данных (например, в таблицу non_working_hours_requests)
        # Здесь нужно добавить логику для сохранения запроса
        save_non_working_hours_request(user_id, message.from_user.username)
        return

    # Добавляем запрос на диалог
    add_chat_request(user_id)

    # Создаем клавиатуру с кнопкой "Закончить диалог"
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Закончить диалог")]],
                                         resize_keyboard=True)
    await message.answer("⏳ Пожалуйста, подождите, пока специалист освободится.", reply_markup=keyboard)

    # Отправляем уведомление всем администраторам
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Принять", callback_data=f"accept_{user_id}")

    for admin_id in ADMINS:
        if not get_chat_request_for_admin(admin_id):
            sent_message = await message.bot.send_message(
                admin_id,
                f"Пользователь @{message.from_user.username} хочет начать диалог.",
                reply_markup=builder.as_markup()
            )
            # Сохраняем message_id уведомления
            add_admin_notification(admin_id, sent_message.message_id)

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

    # Удаляем уведомления у остальных администраторов
    for other_admin_id in ADMINS:
        if other_admin_id != admin_id:
            message_ids = get_admin_notifications(other_admin_id)
            for message_id in message_ids:
                try:
                    await call.bot.delete_message(other_admin_id, message_id)
                except Exception as e:
                    print(f"Не удалось удалить сообщение у администратора {other_admin_id}: {e}")
            delete_admin_notifications(other_admin_id)

    # Уведомляем остальных администраторов
    for other_admin_id in ADMINS:
        if other_admin_id != admin_id:
            await call.bot.send_message(other_admin_id, f"Диалог с пользователем уже ведет другой администратор.")

@router.message(F.text == "❌ Закончить диалог")
async def end_chat_command(message: types.Message):
    user_id = message.from_user.id

    try:
        if user_id in ADMINS:
            admin_id = get_chat_request_for_admin(user_id)
            user_id, admin_id = admin_id, user_id
            end_chat(user_id)
            await message.bot.send_message(admin_id, "❌ Диалог завершен.", reply_markup=get_main_menu(admin_id))
            await message.bot.send_message(user_id, "❌ Диалог завершен.")
            await message.bot.send_message(user_id, "Администратор завершил диалог.", reply_markup=get_main_menu(user_id))
        else:
            admin_id = get_chat_request(user_id)
            if not admin_id:
                await message.answer("❌ Диалог завершен.", reply_markup=get_main_menu(user_id))
                for admin_id in ADMINS:
                    message_ids = get_admin_notifications(admin_id)
                    for message_id in message_ids:
                        try:
                            await message.bot.delete_message(admin_id, message_id)
                        except Exception as e:
                            print(f"Не удалось удалить сообщение у администратора {admin_id}: {e}")
                    delete_admin_notifications(admin_id)
                return
            end_chat(user_id)
            await message.bot.send_message(admin_id, "❌ Диалог завершен.")
            await message.bot.send_message(admin_id, f"Пользователь @{message.from_user.username} завершил диалог.", reply_markup=get_main_menu(admin_id))
            await message.bot.send_message(user_id, "❌ Диалог завершен.", reply_markup=get_main_menu(user_id))
    except:
        pass

@router.message(lambda message: get_chat_request(message.from_user.id))  # Фильтр для сообщений от пользователей в диалоге
async def forward_message_from_user(message: types.Message):
    admin_id = get_chat_request(message.from_user.id)
    if admin_id:
        await message.bot.send_message(admin_id, f"Сообщение от пользователя @{message.from_user.username}:\n{message.text}")

@router.message(lambda message: get_chat_request_for_admin(message.from_user.id))  # Фильтр для сообщений от администраторов в диалоге
async def forward_message_from_admin(message: types.Message):
    user_id = get_chat_request_for_admin(message.from_user.id)
    if user_id:
        await message.bot.send_message(user_id, f"Сообщение от администратора:\n{message.text}")