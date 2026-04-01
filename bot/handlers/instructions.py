from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.keyboards.reply import get_instructions_kb, get_back_to_menu_kb

router = Router()

INSTRUCTIONS = {
    "windows": {
        "title": "🪟 Настройка VPN на Windows",
        "text": (
            "1. Скачайте клиент WireGuard с официального сайта\n"
            "2. Установите приложение\n"
            "3. Нажмите 'Import tunnel(s) from file'\n"
            "4. Вставьте ваш VPN ключ\n"
            "5. Нажмите 'Activate'\n"
            "6. Готово! Вы подключены ✅"
        ),
        "photo": None
    },
    "macos": {
        "title": "🍎 Настройка VPN на macOS",
        "text": (
            "1. Скачайте Tunnelblick с официального сайта\n"
            "2. Установите приложение\n"
            "3. Нажмите 'I have configuration files'\n"
            "4. Откройте файл конфигурации\n"
            "5. Подключитесь к VPN\n"
            "6. Готово! Вы подключены ✅"
        ),
        "photo": None
    },
    "ios": {
        "title": "📱 Настройка VPN на iOS",
        "text": (
            "1. Скачайте WireGuard из App Store\n"
            "2. Откройте приложение\n"
            "3. Нажмите '+' для добавления туннеля\n"
            "4. Выберите 'Create from QR code' или вставьте ключ вручную\n"
            "5. Активируйте туннель\n"
            "6. Готово! Вы подключены ✅"
        ),
        "photo": None
    },
    "android": {
        "title": "🤖 Настройка VPN на Android",
        "text": (
            "1. Скачайте WireGuard из Google Play\n"
            "2. Откройте приложение\n"
            "3. Нажмите '+' для добавления туннеля\n"
            "4. Отсканируйте QR код или вставьте ключ вручную\n"
            "5. Нажмите на туннель для подключения\n"
            "6. Готово! Вы подключены ✅"
        ),
        "photo": None
    }
}


@router.callback_query(F.data == "instructions")
async def show_instructions_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 <b>Инструкции по настройке VPN</b>\n\n"
        "Выберите вашу операционную систему:",
        reply_markup=get_instructions_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("inst_"))
async def show_instruction(callback: CallbackQuery):
    os_type = callback.data.replace("inst_", "")

    if os_type not in INSTRUCTIONS:
        await callback.answer("Инструкция не найдена", show_alert=True)
        return

    instruction = INSTRUCTIONS[os_type]

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад к списку", callback_data="instructions")
    )
    builder.row(
        InlineKeyboardButton(text="🏠 В меню", callback_data="menu")
    )

    if instruction["photo"]:
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=instruction["photo"],
                caption=f"<b>{instruction['title']}</b>\n\n{instruction['text']}",
                parse_mode="HTML"
            ),
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.edit_text(
            f"<b>{instruction['title']}</b>\n\n{instruction['text']}",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

    await callback.answer()
