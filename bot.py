from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from dotenv import load_dotenv
import logging
import asyncio
import os
from handlers import router 

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Проверьте файл .env")

if not ADMIN_ID:
    raise ValueError("ID администратора не найден. Проверьте файл .env")

try:
    ADMIN_ID = int(ADMIN_ID) 
except ValueError:
    raise ValueError("ID администратора должен быть числом.")

class AdminIDMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['admin_id'] = int(os.getenv("ADMIN_ID"))
        return await handler(event, data)
        
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()
dp.include_router(router)
dp.update.outer_middleware(AdminIDMiddleware())

async def main():
    logging.info("Бот запущен и готов к работе.")
    async with bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
