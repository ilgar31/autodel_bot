from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMINS
from database import add_promotion, remove_promotion, get_promotions
from keyboards.main_menu import get_main_menu
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F  # Используем F для фильтрации

router = Router()

class PromoState(StatesGroup):
    waiting_for_promo = State()

@router.message(F.text == "💰 Акции и предложения")  # Фильтруем по тексту сообщения
async def show_promo(message: types.Message):
    promotions = get_promotions()
    if promotions:
        text = "💰 Текущие акции и предложения:\n" + "\n".join(promotions)
    else:
        text = "На данный момент нет активных акций."
    await message.answer(text)

@router.message(F.text == "⚙️ Управление акциями")
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMINS:
        # Создаем список кнопок для клавиатуры
        buttons = [
            [types.KeyboardButton(text="➕ Добавить акцию")],
            [types.KeyboardButton(text="❌ Удалить акцию")],
            [types.KeyboardButton(text="🔙 Назад")]
        ]
        # Создаем клавиатуру с кнопками
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("❌ У вас нет доступа к этой функции.")

@router.message(F.text == "🔙 Назад")
async def admin_cancel(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=get_main_menu(message.chat.id))

@router.message(F.text == "➕ Добавить акцию")
async def add_promo(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Введите текст новой акции:")
        await state.set_state(PromoState.waiting_for_promo)

@router.message(PromoState.waiting_for_promo)
async def receive_promo(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        add_promotion(message.text)
        await message.answer("✅ Акция добавлена!")
        await state.clear()

@router.message(F.text == "❌ Удалить акцию")
async def remove_promo_menu(message: types.Message):
    if message.from_user.id in ADMINS:
        promotions = get_promotions()
        if not promotions:
            await message.answer("❌ Нет акций для удаления.")
            return

        builder = InlineKeyboardBuilder()
        for promo in promotions:
            builder.button(text=promo, callback_data=f"deletepromo_{promo}")
        await message.answer("Выберите акцию для удаления:", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data.startswith("deletepromo_"))  # Обработка callback-запросов
async def remove_promo_callback(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        promo_text = call.data.split("_")[1]
        remove_promotion(promo_text)  # Передаем текст акции
        await call.message.edit_text(f"✅ Акция удалена: {promo_text}")