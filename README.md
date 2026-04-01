# VPN Telegram Bot

Telegram бот для продажи VPN подписок с капчей, оплатой через Plate iO и автоматическими напоминаниями.

## Стек

- Python 3.10+
- aiogram 3.x
- SQLAlchemy 2.x (async)
- Redis (FSM + кеш)
- PostgreSQL / SQLite

## Установка

```bash
# Клонирование
git clone <repo>
cd vpn

# Виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux

# Зависимости
pip install -r requirements.txt
```

## Настройка

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321

# PostgreSQL (или оставьте пустым для SQLite)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=vpn_bot

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Plate iO
PLATEIO_API_KEY=your_api_key
PLATEIO_API_URL=https://api.plate.io
```

## Запуск

```bash
# Создание таблиц и тарифов
python seed.py

# Запуск бота
python -m bot.main
```

## Структура проекта

```
bot/
├── config.py           # Конфигурация
├── main.py             # Точка входа
├── handlers/            # Обработчики
│   ├── start.py        # Капча
│   ├── menu.py        # Главное меню
│   ├── buy.py         # Покупка подписки
│   ├── profile.py     # Личный кабинет
│   ├── instructions.py # Инструкции
│   └── support.py     # Поддержка
├── keyboards/         # Inline клавиатуры
├── services/          # Бизнес-логика
│   ├── payments.py    # Plate iO API
│   ├── vpn.py         # Генерация ключей
│   └── notifications.py # Напоминания
├── database/          # Работа с БД
│   ├── models.py     # SQLAlchemy модели
│   └── queries.py     # ORM запросы
├── states/            # FSM состояния
└── middlewares/       # Middleware
```

## Функционал

### Капча
- Математический пример (a+b)
- 3 попытки
- Блокировка при неудаче

### Покупка подписки
- Выбор тарифа из БД
- Оплата через Plate iO
- Автоматическое создание подписки

### Напоминания
- 5 мин - первое напоминание
- 60 мин - второе + выдача 3 дней бесплатно

### Личный кабинет
- Статус подписки
- VPN ключ
- Инструкции

## Команды бота

- `/start` - Начало работы + капча

## База данных

### Таблицы

- `users` - пользователи
- `tariffs` - тарифы
- `subscriptions` - подписки
- `payments` - платежи

## Production запуск

```bash
# Supervisor
[program:vpn-bot]
command=/path/to/venv/bin/python -m bot.main
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

## Лицензия

MIT
