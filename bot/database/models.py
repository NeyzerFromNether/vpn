from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.pool import NullPool

from bot.config import config

Base = declarative_base()

if config.db.host == "localhost" and config.db.user == "postgres":
    DB_URL = "sqlite+aiosqlite:///./vpn_bot.db"
else:
    DB_URL = config.db.url

engine = create_async_engine(DB_URL, echo=False, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    captcha_passed = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    subscriptions = relationship("Subscription", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, nullable=False)
    description = Column(Text)

    subscriptions = relationship("Subscription", back_populates="tariff")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="active")
    vpn_key = Column(String(255), nullable=True)

    user = relationship("User", back_populates="subscriptions")
    tariff = relationship("Tariff", back_populates="subscriptions")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_id = Column(String(255), nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="payments")
    tariff = relationship("Tariff")
