from aiogram import Router, types
from database import get_subscribers
from config import ADMINS
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F  # Используем F для фильтрации

router = Router()

class PromoState(StatesGroup):
    waiting_message_for_users = State()

@router.message(F.text == "✉️ Создать рассылку")
async def broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    await message.answer("Введите текст для рассылки:")
    await state.set_state(PromoState.waiting_message_for_users)

@router.message(PromoState.waiting_message_for_users)
async def broadcast_message(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        if not message.text:
            await message.answer("❌ Укажите текст для рассылки.")
            return

        subscribers = get_subscribers()

        for user_id in subscribers:
            try:
                await message.bot.send_message(user_id, message.text)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        await message.answer(f"✅ Рассылка завершена. Сообщение отправлено всем пользователям.")
        await state.clear()