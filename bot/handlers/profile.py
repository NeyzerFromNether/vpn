from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime

from bot.database.queries import get_user_subscription, get_user
from bot.database.models import async_session_maker
from bot.keyboards.reply import get_profile_kb

router = Router()


@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with async_session_maker() as session:
        user = await get_user(session, user_id)
        subscription = await get_user_subscription(session, user_id)

    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    text = f"👤 <b>Личный кабинет</b>\n\n"
    text += f"🆔 ID: {user.id}\n"
    text += f"📛 Username: @{user.username or 'Не указан'}\n"
    text += f"📅 Регистрация: {user.registration_date.strftime('%d.%m.%Y')}\n\n"

    if subscription:
        days_left = (subscription.end_date - datetime.utcnow()).days
        text += f"📦 <b>Подписка:</b>\n"
        text += f"   Статус: ✅ Активна\n"
        text += f"   Тариф: {subscription.tariff.name}\n"
        text += f"   Осталось: {days_left} дн.\n"
        text += f"   Истекает: {subscription.end_date.strftime('%d.%m.%Y')}\n\n"
        text += f"🔑 <b>VPN ключ:</b>\n"
        text += f"<code>{subscription.vpn_key}</code>"
    else:
        text += "📦 <b>Подписка:</b>\n"
        text += "   Статус: ❌ Нет активной подписки\n\n"
        text += "🛒 Хотите приобрести подписку?"

    await callback.message.edit_text(
        text,
        reply_markup=get_profile_kb(),
        parse_mode="HTML"
    )
    await callback.answer()
