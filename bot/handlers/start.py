import random
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states.buy_states import CaptchaStates
from bot.database.queries import create_user, get_user, update_captcha_status
from bot.database.models import async_session_maker

router = Router()


def generate_captcha() -> tuple[str, int]:
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a}+{b}", a + b


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    async with async_session_maker() as session:
        user = await get_user(session, user_id)
        if not user:
            user = await create_user(session, user_id, username)

        if user.is_blocked:
            await message.answer("⛔ Вы заблокированы.")
            return

        if user.captcha_passed:
            from bot.keyboards.reply import get_main_menu_kb
            await message.answer(
                "👋 Добро пожаловать! Вы уже прошли верификацию.",
                reply_markup=get_main_menu_kb()
            )
            return

    question, answer = generate_captcha()
    await state.update_data(captcha_answer=answer, attempts=3)
    await state.set_state(CaptchaStates.waiting_answer)

    await message.answer(
        f"🔐 Пожалуйста, решите пример для верификации:\n\n"
        f"<b>{question} = ?</b>\n\n"
        f"У вас 3 попытки.",
        parse_mode="HTML"
    )


@router.message(CaptchaStates.waiting_answer)
async def process_captcha(message: Message, state: FSMContext):
    text = message.text.strip()
    state_data = await state.get_data()
    correct_answer = state_data.get("captcha_answer")
    attempts = state_data.get("attempts", 3)

    try:
        user_answer = int(text)
    except ValueError:
        await message.answer("❌ Введите число!")
        return

    if user_answer == correct_answer:
        await state.clear()

        async with async_session_maker() as session:
            await update_captcha_status(session, message.from_user.id, passed=True)

        await message.answer("✅ Верификация пройдена!")
        from bot.keyboards.reply import get_main_menu_kb
        await message.answer(
            "🏠 <b>Главное меню</b>",
            reply_markup=get_main_menu_kb(),
            parse_mode="HTML"
        )
    else:
        attempts -= 1

        if attempts <= 0:
            await state.clear()

            async with async_session_maker() as session:
                await update_captcha_status(session, message.from_user.id, passed=False, blocked=True)

            await message.answer("⛔ Вы заблокированы за превышение попыток.")
        else:
            question, answer = generate_captcha()
            await state.update_data(captcha_answer=answer, attempts=attempts)
            await message.answer(
                f"❌ Неверно!\n\n"
                f"🔐 Новый пример:\n<b>{question}</b>\n\n"
                f"Осталось попыток: {attempts}",
                parse_mode="HTML"
            )
