from aiogram import Router, types
from aiogram import F  # Используем F для фильтрации
from config import ADMINS

router = Router()

@router.message(F.content_type == "contact")  # Фильтруем по типу контента
async def receive_contact(message: types.Message):
    await message.answer("✅ Спасибо! Администратор свяжется с вами.")
    for admin_id in ADMINS:
        print(admin_id)
        await message.bot.send_message(admin_id, f"Пользователь оставил свои контактные данные для обратной связи.\n\n👤 Имя: {message.contact.first_name}\n☎️ Контакт: {message.contact.phone_number}\n📱 Telegram: @{message.from_user.username}")