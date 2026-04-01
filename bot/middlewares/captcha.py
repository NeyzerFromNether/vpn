from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.database.queries import get_user
from bot.database.models import async_session_maker


class CaptchaMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message) or isinstance(event, CallbackQuery):
            user_id = event.from_user.id

            async with async_session_maker() as session:
                user = await get_user(session, user_id)

            if user and not user.is_blocked and user.captcha_passed:
                return await handler(event, data)

        return await handler(event, data)
