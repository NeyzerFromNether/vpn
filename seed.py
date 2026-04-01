import asyncio
from sqlalchemy import select

from bot.database.models import init_db, async_session_maker, Tariff


async def seed_tariffs():
    await init_db()

    default_tariffs = [
        Tariff(
            name="Basic",
            price=4.99,
            duration_days=30,
            description="Базовая подписка на 1 месяц"
        ),
        Tariff(
            name="Premium",
            price=12.99,
            duration_days=90,
            description="Премиум подписка на 3 месяца"
        ),
        Tariff(
            name="Ultimate",
            price=39.99,
            duration_days=365,
            description="Максимальная подписка на 1 год"
        ),
    ]

    async with async_session_maker() as session:
        for tariff in default_tariffs:
            existing = await session.execute(
                select(Tariff).where(Tariff.name == tariff.name)
            )
            if not existing.scalar_one_or_none():
                session.add(tariff)

        await session.commit()

    print("Tariffs seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_tariffs())
