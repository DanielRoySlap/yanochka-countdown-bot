import asyncio
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot

START_DATE = date(2026, 7, 4)
ARRIVAL_DATE = date(2026, 9, 8)
TOTAL_DAYS = 67
IMAGES_DIR = Path(__file__).parent / "images"


def plural_days(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "дней"
    last = n % 10
    if last == 1:
        return "день"
    if 2 <= last <= 4:
        return "дня"
    return "дней"


def get_countdown(today: date | None = None) -> tuple[int, int, str] | None:
    today = today or date.today()

    if today < START_DATE or today > ARRIVAL_DATE:
        return None

    day_number = (today - START_DATE).days + 1
    days_left = TOTAL_DAYS - day_number + 1

    if today == ARRIVAL_DATE:
        caption = "Сегодня приезжает Яночка! 💕"
    else:
        caption = f"Осталось {days_left} {plural_days(days_left)} до приезда Яночки 💕"

    return day_number, days_left, caption


def get_image_path(day_number: int) -> Path:
    return IMAGES_DIR / f"day_{day_number:02d}.png"


async def send_daily_message() -> None:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        print("Ошибка: задайте BOT_TOKEN и CHAT_ID в переменных окружения", file=sys.stderr)
        sys.exit(1)

    countdown = get_countdown()
    if countdown is None:
        print(f"Сегодня ({date.today()}) вне периода обратного отсчёта, сообщение не отправлено")
        return

    day_number, _days_left, caption = countdown
    image_path = get_image_path(day_number)

    if not image_path.exists():
        print(f"Ошибка: файл {image_path} не найден", file=sys.stderr)
        sys.exit(1)

    bot = Bot(token=bot_token)
    with image_path.open("rb") as photo:
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)

    print(f"Сообщение отправлено: день {day_number}, «{caption}»")


if __name__ == "__main__":
    asyncio.run(send_daily_message())
