import uuid
from typing import Optional
from bot.config import config


async def create_payment(user_id: int, amount: float, tariff_id: int) -> dict:
    payment_id = str(uuid.uuid4())
    
    return {
        "payment_id": payment_id,
        "amount": amount,
        "currency": "USD",
        "status": "pending",
        "checkout_url": f"https://plate.io/pay/{payment_id}",
        "mock": True
    }


async def check_payment_status(payment_id: str) -> dict:
    return {
        "payment_id": payment_id,
        "status": "pending",
        "mock": True
    }
