from aiogram.fsm.state import State, StatesGroup


class CaptchaStates(StatesGroup):
    waiting_answer = State()


class BuyStates(StatesGroup):
    selecting_tariff = State()
    selecting_payment_method = State()
    waiting_payment = State()


class ProfileStates(StatesGroup):
    viewing = State()
