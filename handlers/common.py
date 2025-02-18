from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(StateFilter(None))  # Обрабатываем только сообщения вне состояний
async def unknown_message(message: types.Message):
    await message.answer("Извините, я вас не понимаю. Используйте кнопки меню.")