from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu
from database import add_subscriber

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    add_subscriber(user_id)
    text = '''
Добро пожаловать в чат-бот Автодель! 🚗

Мы - самый крупный автомобильный дилер на территории Крыма, предлагающий легковой и коммерческий транспорт ведущих мировых брендов, сервисное обслуживание, тюнинг и услуги trade-in. Наш бот поможет вам быстро и удобно:

🔹 Выбрать дилерский центр по интересующему бренду
🔹 Узнать актуальные акции и предложения
🔹 Оставить номер для связи, чтобы наш менеджер перезвонил вам
🔹 Связаться с администратором для получения дополнительной информации

Выберите нужный раздел в меню и получите всю необходимую информацию в несколько кликов! 🚀'''
    await message.answer(text, reply_markup=get_main_menu(message.chat.id))