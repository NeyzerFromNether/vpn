import asyncio
from aiogram import Bot

from bot.database.queries import (
    get_pending_payments,
    update_payment_status,
    give_free_days,
    get_payment
)
from bot.services.vpn import generate_key
from bot.database.models import async_session_maker


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_reminder(self, user_id: int, minutes_passed: int):
        text = (
            f"⏰ Напоминание!\n"
            f"Вы не оплатили подписку ({minutes_passed} минут назад).\n"
            f"Пожалуйста, завершите оплату или подписка будет активирована бесплатно на 3 дня."
        )
        await self.bot.send_message(user_id, text)

    async def give_free_subscription(self, user_id: int, tariff_id: int):
        vpn_key = generate_key()
        async with async_session_maker() as session:
            await give_free_days(session, user_id, 3, tariff_id, vpn_key)
        await self.bot.send_message(
            user_id,
            "🎁 Поскольку вы не оплатили подписку вовремя, "
            "мы начислили вам 3 дня бесплатно!\n"
            f"🔑 Ваш VPN ключ: `{vpn_key}`",
            parse_mode="Markdown"
        )

    async def check_unpaid_payments(self):
        async with async_session_maker() as session:
            for payment in await get_pending_payments(session, 5):
                await self.send_reminder(payment.user_id, 5)

            for payment in await get_pending_payments(session, 60):
                await self.send_reminder(payment.user_id, 60)
                payment_obj = await get_payment(session, payment.payment_id)
                if payment_obj:
                    await update_payment_status(session, payment.payment_id, "expired")
                    await self.give_free_subscription(payment.user_id, payment.tariff_id)


async def payment_checker_task(bot: Bot):
    service = NotificationService(bot)
    while True:
        await asyncio.sleep(60)
        try:
            await service.check_unpaid_payments()
        except Exception as e:
            print(f"Error in payment checker: {e}")
