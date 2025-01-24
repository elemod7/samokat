from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from utils import save_to_csv, normalize_phone_number
import logging

router = Router()

WELCOME_TEXT_TEMPLATE = (
    "Предлагаем Вам возможность заработать в компании «Самокат» 💸\n"
    "Условия:\n"
    "⏬ до 220000₽ в месяц\n"
    "⏬ от 5200₽ за полный день\n"
    "⏬ Выплаты КАЖДЫЙ ДЕНЬ!\n"
    "⏬ Есть место для отдыха, еды, зарядки электроники, кулер с водой и туалет\n"
    "💫 Можем выдать велосипед\n"
    "💫 График устанавливаете Вы\n"
    "💫 Любой район города\n"
    "Всё что требуется это 📱 телефон, и Вы можете приступить к заработкам уже сегодня!\n"
    "Напишите Ваш номер телефона в ответ, и мы свяжемся с Вами в ближайшее время для начала сотрудничества и ответим на любые вопросы."
)

@router.message(F.text == "/start")
async def send_welcome(message: Message):
    user_name = message.from_user.first_name
    if user_name:
        welcome_text = f"Доброго дня, {user_name}!\n\n{WELCOME_TEXT_TEMPLATE}"
    else:
        welcome_text = f"Доброго дня!\n\n{WELCOME_TEXT_TEMPLATE}"
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться номером телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(welcome_text, reply_markup=contact_keyboard)

@router.message(F.text == "Возрастные ограничения")
async def handle_age_restrictions(message: Message):
    await message.answer("Возраст от 18 лет.")

@router.message(F.text == "Наличие гражданства")
async def handle_citizenship(message: Message):
    await message.answer("Принимаем граждан стран: РФ, Казахстан, Армения, Беларусь, Киргизия.")

@router.message(F.text == "Города присутствия")
async def handle_cities(message: Message):
    await message.answer(
        "Санкт-Петербург, Москва, Новосибирск, Барнаул, Тула, Калуга, Казань, Уфа, Череповец, "
        "Ногинск, Орехово-Зуево, Краснодар, Ростов, Нижний Новгород, Тюмень, Коломны."
    )

@router.message(F.text == "Вернуться в главное меню")
async def return_to_main_menu(message: Message):
    await send_welcome(message)

@router.message(F.text)
async def get_phone_number(message: Message, bot, admin_id: int):
    user_id, user_name, text = message.from_user.id, message.from_user.first_name, message.text
    normalized_number = normalize_phone_number(text)
    if normalized_number:
        save_to_csv(user_id, user_name, normalized_number, text)
        notification = (
            f"Новый номер от {user_name or 'пользователь'} (ID: {user_id}):\n"
            f"Введённый: {text}\nНормализованный: {normalized_number}"
        )
        try:
            await bot.send_message(admin_id, notification)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение админу: {e}")
        await message.answer(f"Спасибо! Ваш номер {normalized_number} принят. Мы скоро с вами свяжемся!")
    else:
        menu_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Возрастные ограничения")],
                [KeyboardButton(text="Наличие гражданства")],
                [KeyboardButton(text="Города присутствия")],
                [KeyboardButton(text="Вернуться в главное меню")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "Если у Вас есть дополнительные вопросы, то Вы можете выбрать подходящий пункт меню или оставить свой номер телефона, и мы свяжемся с Вами в ближайшее время.",
            reply_markup=menu_keyboard
        )

@router.message(F.contact)
async def handle_contact(message: Message, bot, admin_id: int):
    if message.contact:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        phone_number = message.contact.phone_number
        save_to_csv(user_id, user_name, phone_number, "Отправлен через кнопку 'Поделиться номером'")
        notification = (
            f"Новый контакт от {user_name or 'пользователь'} (ID: {user_id}):\n"
            f"Номер телефона: {phone_number}"
        )
        try:
            await bot.send_message(admin_id, notification)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение админу: {e}")

        await message.answer("Спасибо! Ваш номер успешно отправлен.")
    else:
        await message.answer("Пожалуйста, используйте кнопку 'Поделиться номером телефона'.")

@router.message(F.text == "Возрастные ограничения")
async def handle_age_restrictions(message: Message):
    await message.answer("Возраст от 18 лет.")

@router.message(F.text == "Наличие гражданства")
async def handle_citizenship(message: Message):
    await message.answer("Принимаем граждан стран: РФ, Казахстан, Армения, Беларусь, Киргизия.")

@router.message(F.text == "Города присутствия")
async def handle_cities(message: Message):
    await message.answer(
        "Санкт-Петербург, Москва, Новосибирск, Барнаул, Тула, Калуга, Казань, Уфа, Череповец, "
        "Ногинск, Орехово-Зуево, Краснодар, Ростов, Нижний Новгород, Тюмень, Коломны."
    )

@router.message(F.text == "Вернуться в главное меню")
async def return_to_main_menu(message: Message):
    await send_welcome(message)


