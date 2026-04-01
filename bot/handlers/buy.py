from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.states.buy_states import BuyStates
from bot.database.queries import get_tariffs, get_tariff, create_payment
from bot.database.models import async_session_maker
from bot.services.payments import create_payment as create_plate_payment
from bot.keyboards.reply import get_back_to_menu_kb

router = Router()


@router.callback_query(F.data == "buy")
async def show_tariffs(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        tariffs = await get_tariffs(session)

    if not tariffs:
        await callback.answer("Нет доступных тарифов", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    for tariff in tariffs:
        builder.row(
            InlineKeyboardButton(
                text=f"{tariff.name} - ${tariff.price}/ {tariff.duration_days} дн.",
                callback_data=f"tariff_{tariff.id}"
            )
        )
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu")
    )

    await callback.message.edit_text(
        "🛒 <b>Выберите тариф:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(BuyStates.selecting_tariff)
    await callback.answer()


@router.callback_query(F.data.startswith("tariff_"))
async def select_tariff(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(selected_tariff_id=tariff_id)

    async with async_session_maker() as session:
        tariff = await get_tariff(session, tariff_id)

    if not tariff:
        await callback.answer("Тариф не найден", show_alert=True)
        return

    from bot.keyboards.reply import get_payment_methods_kb
    await callback.message.edit_text(
        f"📦 <b>Выбран тариф:</b> {tariff.name}\n"
        f"💰 Цена: ${tariff.price}\n"
        f"⏱ Длительность: {tariff.duration_days} дней\n\n"
        f"{tariff.description or ''}\n\n"
        f"Выберите способ оплаты:",
        reply_markup=get_payment_methods_kb(tariff_id),
        parse_mode="HTML"
    )
    await state.set_state(BuyStates.selecting_payment_method)
    await callback.answer()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    tariff_id = int(parts[2])

    async with async_session_maker() as session:
        tariff = await get_tariff(session, tariff_id)

    if not tariff:
        await callback.answer("Тариф не найден", show_alert=True)
        return

    user_id = callback.from_user.id
    payment_data = await create_plate_payment(user_id, float(tariff.price), tariff_id)

    async with async_session_maker() as session:
        await create_payment(session, user_id, tariff_id, float(tariff.price), payment_data["payment_id"])

    await state.update_data(
        payment_id=payment_data["payment_id"],
        tariff_id=tariff_id,
        amount=float(tariff.price)
    )

    await callback.message.edit_text(
        f"💳 <b>Платеж создан!</b>\n\n"
        f"📦 Тариф: {tariff.name}\n"
        f"💰 Сумма: ${tariff.price}\n"
        f"🆔 ID: {payment_data['payment_id']}\n\n"
        f"⏳ Ожидание оплаты...\n\n"
        f"💡 <i>После оплаты нажмите кнопку ниже для проверки</i>",
        reply_markup=InlineKeyboardBuilder().row(
            InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_payment"),
            InlineKeyboardButton(text="🔙 Отмена", callback_data="menu")
        ).as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(BuyStates.waiting_payment)
    await callback.answer()


@router.callback_query(F.data == "check_payment")
async def check_payment(callback: CallbackQuery, state: FSMContext):
    from bot.database.queries import get_payment, create_subscription
    from bot.services.vpn import generate_key

    state_data = await state.get_data()
    payment_id = state_data.get("payment_id")
    tariff_id = state_data.get("tariff_id")

    async with async_session_maker() as session:
        payment = await get_payment(session, payment_id)

        if not payment:
            await callback.answer("Платеж не найден", show_alert=True)
            return

        if payment.status == "success":
            vpn_key = generate_key()
            await create_subscription(session, payment.user_id, tariff_id, vpn_key, payment.tariff.duration_days)

            await callback.message.edit_text(
                f"🎉 <b>Оплата прошла успешно!</b>\n\n"
                f"✅ Подписка активирована\n"
                f"📅 Срок: {payment.tariff.duration_days} дней\n\n"
                f"🔑 <b>Ваш VPN ключ:</b>\n"
                f"<code>{vpn_key}</code>\n\n"
                f"📚 Нажмите 'Инструкция' для настройки",
                reply_markup=InlineKeyboardBuilder().row(
                    InlineKeyboardButton(text="📚 Инструкция", callback_data="instructions"),
                    InlineKeyboardButton(text="🏠 Меню", callback_data="menu")
                ).as_markup(),
                parse_mode="HTML"
            )
            await state.clear()
        else:
            await callback.answer("Оплата еще не поступила. Попробуйте позже.", show_alert=True)
