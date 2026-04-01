import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import config
from bot.database.models import init_db
from bot.handlers import start, menu, buy, profile, instructions, support
from bot.middlewares.captcha import CaptchaMiddleware
from bot.services.notifications import payment_checker_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def register_routers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        menu.router,
        buy.router,
        profile.router,
        instructions.router,
        support.router
    )


async def main():
    bot = Bot(token=config.bot.bot_token)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.message.middleware(CaptchaMiddleware())
    dp.callback_query.middleware(CaptchaMiddleware())

    await register_routers(dp)
    await init_db()

    asyncio.create_task(payment_checker_task(bot))

    logger.info("Bot starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
