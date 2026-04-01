from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🛒 Купить подписку", callback_data="buy")
    )
    builder.row(
        InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Инструкции", callback_data="instructions")
    )
    builder.row(
        InlineKeyboardButton(text="❓ Поддержка", callback_data="support")
    )
    builder.row(
        InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")
    )
    return builder.as_markup()


def get_back_to_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu")
    )
    return builder.as_markup()


def get_instructions_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🪟 Windows", callback_data="inst_windows")
    )
    builder.row(
        InlineKeyboardButton(text="🍎 macOS", callback_data="inst_macos")
    )
    builder.row(
        InlineKeyboardButton(text="📱 iOS", callback_data="inst_ios")
    )
    builder.row(
        InlineKeyboardButton(text="🤖 Android", callback_data="inst_android")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu")
    )
    return builder.as_markup()


def get_support_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📚 Инструкция", callback_data="instructions")
    )
    builder.row(
        InlineKeyboardButton(text="💬 Связаться с админом", url="https://t.me/your_admin_username")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu")
    )
    return builder.as_markup()


def get_payment_methods_kb(tariff_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Банковская карта", callback_data=f"pay_card_{tariff_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🪙 Криптовалюта", callback_data=f"pay_crypto_{tariff_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="buy")
    )
    return builder.as_markup()


def get_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📚 Инструкция", callback_data="instructions")
    )
    builder.row(
        InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu")
    )
    return builder.as_markup()
