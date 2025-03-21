from aiogram import Router, types
from aiogram import F  # Используем F для фильтрации
import random
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
import time
from aiogram.types import BufferedInputFile
from keyboards.main_menu import get_main_menu
from aiogram.fsm.context import FSMContext
from config import ADMINS

router = Router()

dealers = {
    "Москвич": {
        "phone": "+7 (978) 835-38-35",
        "description": 'Официальный дилер автомобилей "Москвич". Мы предлагаем современные и надежные автомобили, созданные с учетом потребностей российских дорог. Идеальный выбор для тех, кто ценит комфорт и доступность.',
        "photo": "photos/Москвич.jpg",
        "car": "cars/Москвич.png",
        "address": "г. Симферополь, ул. Киевская, 187"
    },
    "BMW": {
        "phone": "+7 (978) 835-38-35",
        "description": "Дилерский центр BMW — это сочетание роскоши, инноваций и высоких технологий. Мы предлагаем автомобили, которые подчеркивают ваш статус и обеспечивают непревзойденное удовольствие от вождения.",
        "photo": "photos/BMW.jpg",
        "car": "cars/BMW.png",
        "address": "г. Симферополь, пр. Победы, 110"
    },
    "Hyundai": {
        "phone": "+7 (978) 835-70-07",
        "description": "Официальный дилер Hyundai. Автомобили Hyundai — это надежность, стиль и передовые технологии по доступной цене. Мы заботимся о вашем комфорте и безопасности на дороге.",
        "photo": "photos/Hyundai.jpg",
        "car": "cars/Hyundai.jpg",
        "address": "г. Симферополь, улица Киевская, 187-В"
    },
    "Kaiyi": {
        "phone": "+7 (978) 771-00-00",
        "description": "Добро пожаловать в дилерский центр Kaiyi! Мы предлагаем современные и стильные автомобили, которые сочетают в себе высокое качество, доступность и инновационные решения.",
        "photo": "photos/Kaiyi.jpg",
        "car": "cars/Kaiyi.jpg",
        "address": "г. Симферополь, пр. Победы, 110"
    },
    "Soueast": {
        "phone": "+7 (978) 774-03-03",
        "description": "Официальный дилер Soueast. Мы предлагаем автомобили, которые идеально подходят для городских поездок и дальних путешествий. Надежность и комфорт — наш приоритет.",
        "photo": "photos/Soueast.jpg",
        "car": "cars/Soueast.jpeg",
        "address": "г. Симферополь, пр. Победы, 110"
    },
    "Jetour": {
        "phone": "+7 (978) 752-40-00",
        "description": "Дилерский центр Jetour. Мы предлагаем автомобили, которые выделяются своим стилем, технологичностью и надежностью. Jetour — это идеальный выбор для активных и современных водителей.",
        "photo": "photos/Jetour.jpg",
        "car": "cars/Jetour.png",
        "address": "г. Симферополь, ул. Киевская 187"
    },
    "Evolute": {
        "phone": "+7 (978) 755-00-30",
        "description": "Официальный дилер Evolute. Мы предлагаем инновационные электромобили, которые сочетают в себе экологичность, современный дизайн и передовые технологии.",
        "photo": "photos/Evolute.jpg",
        "car": "cars/Evolute.png",
        "address": "г. Симферополь, ул. Киевская, 187"
    },
    "Lexus": {
        "phone": "+7 (978) 755-00-30",
        "description": "Сервисный центр Lexus — это эталон качества обслуживания и заботы о вашем автомобиле. Мы предлагаем профессиональный сервис, который обеспечивает надежность, комфорт и долговечность вашего автомобиля. Доверьтесь нам, чтобы ваш Lexus всегда оставался в идеальном состоянии.",
        "photo": "photos/Lexus.jpg",
        "car": "cars/Lexus.jpg",
        "address": "г. Симферополь, ул. Киевская, 187"
    },
    "Gaz": {
        "phone": "+7 (3652) 88-74-58",
        "description": "Официальный дилер автомобилей GAZ. Мы предлагаем надежные и практичные автомобили, которые идеально подходят для работы и повседневной жизни.",
        "photo": "photos/Gaz.png",
        "car": "cars/Gaz.jpg",
        "address": "Республика Крым, Белоглинка, ул. Салгирная, 10-А"
    },
    "Jac": {
        "phone": "+7 (3652) 77-94-13",
        "description": "Добро пожаловать в дилерский центр JAC! Мы предлагаем автомобили, которые сочетают в себе доступность, надежность и современный дизайн. Идеальный выбор для города и путешествий.",
        "photo": "photos/Jac.jpg",
        "car": "cars/JAC.png",
        "address": "Республика Крым, Белоглинка, ул. Салгирная, 10-А"
    },
    "Solaris": {
        "phone": "+7 (978) 835-70-07",
        "description": "Официальный дилер Solaris. Мы предлагаем автомобили, которые выделяются своим стилем, комфортом и доступностью. Solaris — ваш надежный партнер на дороге.",
        "photo": "photos/Solaris.jpg",
        "car": "cars/Solaris.jpg",
        "address": "г. Симферополь, ул. Киевская, 187, корп. 1"
    },
    "УАЗ": {
        "phone": "+7 (978) 000-10-80",
        "description": "Дилерский центр УАЗ. Мы предлагаем легендарные внедорожники, которые подходят для любых дорожных условий. УАЗ — это надежность и мощь в каждой поездке.",
        "photo": "photos/УАЗ.jpg",
        "car": "cars/УАЗ.png",
        "address": "г. Симферополь, ул. Киевская, 187 литера В"
    },
    "Voyah": {
        "phone": "+7 (978) 755-00-30",
        "description": "Официальный дилер Voyah. Мы предлагаем инновационные автомобили, которые сочетают в себе роскошь, экологичность и передовые технологии. Voyah — это будущее на дорогах.",
        "photo": "photos/Voyah.png",
        "car": "cars/Voyah.png",
        "address": "г. Симферополь, ул. Киевская 187"
    },
    "Dongfeng": {
        "phone": "+7 (978) 877-10-00",
        "description": "Добро пожаловать в дилерский центр Dongfeng! Мы предлагаем автомобили, которые сочетают в себе доступность, надежность и современный дизайн. Идеальный выбор для города и путешествий.",
        "photo": "photos/Dongfeng.jpg",
        "car": "cars/Dongfeng.png",
        "address": "г. Симферополь, ул. Киевская, 187-В"
    },
    # "Geely": {
    #     "phone": "+7 (978) 818-01-01",
    #     "description": "Официальный дилер Geely. Мы предлагаем стильные и технологичные автомобили, которые подчеркивают ваш статус и обеспечивают комфорт на дороге.",
    #     "photo": "photos/Geely.jpg",
    #    "car": "cars/",
    #    "address": ""
    # },
    "Sollers": {
        "phone": "+7 (978) 311-10-10",
        "description": "Дилерский центр Sollers. Мы предлагаем автомобили, которые идеально подходят для работы и отдыха. Надежность и практичность — наш приоритет.",
        "photo": "photos/Sollers.jpg",
        "car": "cars/Sollers.png",
        "address": "Республика Крым, Белоглинка, ул. Салгирная, 10-А"
    },
    "Toyota": {
        "phone": "+7 (978) 788-00-30",
        "description": "Сервисный центр Toyota — это гарантия надежности и профессионализма. Мы предлагаем полный спектр услуг по техническому обслуживанию и ремонту автомобилей Toyota. Наши высококвалифицированные специалисты используют оригинальные запчасти и современное оборудование, чтобы ваш автомобиль всегда оставался в отличном состоянии.",
        "photo": "photos/Toyota.jpg",
        "car": "cars/Toyota.jpg",
        "address": "г. Симферополь, ул. Киевская, 187"
    },
    "Nissan": {
        "phone": "+7 (978) 836-08-08",
        "description": "Сервисный центр Nissan — это сочетание передовых технологий и высокого качества обслуживания. Мы предоставляем комплексные услуги по диагностике, ремонту и техническому обслуживанию автомобилей Nissan. Наша команда профессионалов обеспечивает максимальную заботу о вашем автомобиле, чтобы он всегда радовал вас своей надежностью и комфортом.",
        "photo": "photos/Nissan.jpg",
        "car": "cars/Nissan.jpg",
        "address": "г. Симферополь, ул. Киевская, 187"
    },
}

@router.message(F.text == "🎲 Кубик")  # Фильтруем по тексту сообщения
async def roll_dice(message: types.Message):
    brand = random.choice(list(dealers.keys()))
    await message.answer_dice()
    time.sleep(2)
    dealer_info = dealers[brand]
    photo_path = dealer_info["car"]

    # Читаем файл и создаем BufferedInputFile
    with open(photo_path, "rb") as file:
        photo = BufferedInputFile(file.read(), filename=photo_path)

    caption = (
        f"🎲 Вам выпал дилерский центр {brand}\n"
        f"{dealer_info['description']}\n"
        f"📞 Телефон: {dealer_info['phone']}\n"
        f"📫 Адрес: {dealer_info['address']}"
    )
    await message.answer_photo(
        photo=photo,  # Используем BufferedInputFile
        caption=caption
    )

    time.sleep(1)

    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=f"answer_yes")
    builder.button(text="Нет", callback_data=f"answer_not")


    await message.answer("Хотите оставить заявку, чтобы наш менеджер связался с вами?", reply_markup=builder.as_markup())

@router.callback_query(F.data == "answer_yes")
async def yes_before_func(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить контакт", request_contact=True)],
            [KeyboardButton(text="Отменить")],
        ],
        resize_keyboard=True  # Опционально: автоматически изменяет размер клавиатуры
    )

    # Отправляем сообщение с этой клавиатурой
    await callback.message.answer("Пожалуйста, отправьте ваш контакт:", reply_markup=contact_keyboard)
    await callback.answer()

@router.message(F.text == "Отменить")
async def yes_func(callback: types.CallbackQuery, state: FSMContext):
    await callback.delete()
    await callback.answer("Вы отменили действие!", reply_markup = get_main_menu(callback.from_user.id))


@router.callback_query(F.data == "Отправить контакт")
async def yes_func(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("✅ Спасибо! Администратор свяжется с вами.", reply_markup=get_main_menu(callback.message.from_user.id))
    await callback.answer()
    for admin_id in ADMINS:
        await callback.message.bot.send_message(admin_id, f"Пользователь оставил свои контактные данные для обратной связи.\n\n👤 Имя: {callback.message.contact.first_name}\n☎️ Контакт: {callback.message.contact.phone_number}\n📱 Telegram: @{callback.message.from_user.username}")
        await callback.answer()

@router.callback_query(F.data == "answer_not")
async def no_func(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()