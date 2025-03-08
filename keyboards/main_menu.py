from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMINS

def get_main_menu(user_id):
    # Создаем список кнопок для клавиатуры
    buttons = [
        [KeyboardButton(text="🚗 Выбрать дилерский центр")],
        [KeyboardButton(text="💰 Акции и предложения")],
        [KeyboardButton(text="🎲 Кубик")],
    ]

    if user_id not in ADMINS:
        buttons.append([KeyboardButton(text="📞 Оставить номер для связи", request_contact=True)])
        buttons.append([KeyboardButton(text="📝 Написать администратору")])

    # Если пользователь админ, добавляем кнопку управления акциями
    if user_id in ADMINS:
        # buttons.append([KeyboardButton(text="⚙️ Управление акциями")])
        buttons.append([KeyboardButton(text="✉️ Создать рассылку")])

    # Создаем клавиатуру с кнопками
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard