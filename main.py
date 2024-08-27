import asyncio
from dotenv import load_dotenv  # Import the load_dotenv function
import os


from handlers.admin import admin_router
from handlers.start import start_router
from handlers.reply import reply_router
from handlers.change_username import change_username_route

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(
        start_router,
        admin_router,
        reply_router,
        change_username_route,

    )

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())