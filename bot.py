import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем токен из переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура с кнопками
def main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💰 Донат", callback_data="donate"),
        InlineKeyboardButton("📢 Присоединиться", callback_data="join")
    )
    return keyboard

# Обработка команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Этот бот участвует в краудфандинговом эксперименте.\n\n"
        "📌 Люди могут делать небольшие донаты, чтобы случайный человек получил деньги.\n"
        "📢 Ты можешь участвовать, нажав на кнопку ниже!",
        reply_markup=main_keyboard()
    )

# Обработка нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data)
async def button_handler(callback_query: types.CallbackQuery):
    if callback_query.data == "donate":
        await bot.send_message(
            callback_query.from_user.id,
            "💳 Чтобы сделать донат, отправь криптовалюту на этот адрес:\n\n"
            "`0x123456789ABCDEF123456789ABCDEF123456789A`",
            parse_mode="Markdown"
        )
    elif callback_query.data == "join":
        await bot.send_message(
            callback_query.from_user.id,
            "🔄 Ты добавлен в список участников!\n\n"
            "Каждый новый раунд случайным образом выбирает одного человека."
        )

# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()

