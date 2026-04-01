from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.reply import get_main_menu_kb

router = Router()


@router.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    from bot.keyboards.reply import get_back_to_menu_kb
    await callback.message.edit_text(
        "ℹ️ <b>О нас</b>\n\n"
        "Мы предоставляем быстрый и надежный VPN сервис.\n"
        "Безопасность и конфиденциальность - наш приоритет.\n\n"
        "🌍 Серверы по всему миру\n"
        "⚡ Высокая скорость\n"
        "🔒 Шифрование данных\n"
        "📞 Поддержка 24/7",
        reply_markup=get_back_to_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()
