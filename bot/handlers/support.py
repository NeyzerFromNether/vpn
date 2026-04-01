from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.reply import get_support_kb

router = Router()


@router.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    await callback.message.edit_text(
        "❓ <b>Поддержка</b>\n\n"
        "Мы всегда готовы помочь вам!\n\n"
        "📚 Перед обращением проверьте раздел 'Инструкции' — "
        "возможно, ответ уже там.\n\n"
        "💬 Для связи с админом нажмите кнопку ниже.",
        reply_markup=get_support_kb(),
        parse_mode="HTML"
    )
    await callback.answer()
