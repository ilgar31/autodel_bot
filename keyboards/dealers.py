from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_dealers_keyboard(dealers):
    # Создаем список кнопок для клавиатуры
    buttons = []
    row = []  # Временный список для хранения кнопок в текущем ряду

    for dealer in dealers:
        # Добавляем кнопку в текущий ряд
        row.append(InlineKeyboardButton(text=dealer, callback_data=f"dealer_{dealer}"))

        # Если в ряду уже 2 кнопки, добавляем ряд в buttons и начинаем новый ряд
        if len(row) == 2:
            buttons.append(row)
            row = []

    # Если остались кнопки, которые не вошли в полный ряд, добавляем их
    if row:
        buttons.append(row)

    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard