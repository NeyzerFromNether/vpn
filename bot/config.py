import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    bot_token: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    admin_ids: list[int] = field(default_factory=lambda: [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x])


@dataclass
class DatabaseConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "postgres")
    database: str = os.getenv("DB_NAME", "vpn_bot")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    db: int = int(os.getenv("REDIS_DB", "0"))
    password: Optional[str] = os.getenv("REDIS_PASSWORD")

    @property
    def url(self) -> str:
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


@dataclass
class PlateIoConfig:
    api_key: str = os.getenv("PLATEIO_API_KEY", "YOUR_PLATEIO_API_KEY")
    api_url: str = os.getenv("PLATEIO_API_URL", "https://api.plate.io")


@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    plateio: PlateIoConfig = field(default_factory=PlateIoConfig)


config = Config()
