from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User, Tariff, Subscription, Payment


async def create_user(session: AsyncSession, user_id: int, username: str = None) -> User:
    user = User(id=user_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def update_captcha_status(session: AsyncSession, user_id: int, passed: bool, blocked: bool = False):
    await session.execute(
        update(User).where(User.id == user_id).values(
            captcha_passed=passed,
            is_blocked=blocked
        )
    )
    await session.commit()


async def get_tariffs(session: AsyncSession) -> list[Tariff]:
    result = await session.execute(select(Tariff))
    return list(result.scalars().all())


async def get_tariff(session: AsyncSession, tariff_id: int) -> Optional[Tariff]:
    result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
    return result.scalar_one_or_none()


async def create_payment(
    session: AsyncSession,
    user_id: int,
    tariff_id: int,
    amount: float,
    payment_id: str
) -> Payment:
    payment = Payment(
        user_id=user_id,
        tariff_id=tariff_id,
        amount=amount,
        payment_id=payment_id,
        status="pending"
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


async def get_payment(session: AsyncSession, payment_id: str) -> Optional[Payment]:
    result = await session.execute(select(Payment).where(Payment.payment_id == payment_id))
    return result.scalar_one_or_none()


async def update_payment_status(session: AsyncSession, payment_id: str, status: str):
    update_data = {"status": status}
    if status == "success":
        update_data["paid_at"] = datetime.utcnow()
    await session.execute(
        update(Payment).where(Payment.payment_id == payment_id).values(**update_data)
    )
    await session.commit()


async def create_subscription(
    session: AsyncSession,
    user_id: int,
    tariff_id: int,
    vpn_key: str,
    days: int
) -> Subscription:
    start = datetime.utcnow()
    end = start + timedelta(days=days)
    subscription = Subscription(
        user_id=user_id,
        tariff_id=tariff_id,
        start_date=start,
        end_date=end,
        status="active",
        vpn_key=vpn_key
    )
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return subscription


async def get_user_subscription(session: AsyncSession, user_id: int) -> Optional[Subscription]:
    result = await session.execute(
        select(Subscription)
        .where(Subscription.user_id == user_id)
        .where(Subscription.status == "active")
        .order_by(Subscription.end_date.desc())
    )
    return result.scalar_one_or_none()


async def get_pending_payments(session: AsyncSession, minutes: int) -> list[Payment]:
    threshold = datetime.utcnow() - timedelta(minutes=minutes)
    result = await session.execute(
        select(Payment)
        .where(Payment.status == "pending")
        .where(Payment.created_at <= threshold)
    )
    return list(result.scalars().all())


async def give_free_days(session: AsyncSession, user_id: int, days: int, tariff_id: int, vpn_key: str):
    await create_subscription(session, user_id, tariff_id, vpn_key, days)
