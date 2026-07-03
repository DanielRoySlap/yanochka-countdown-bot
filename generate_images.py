"""Генерирует 67 placeholder-изображений. Замените их на свои картинки с милыми зверятами."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = Path(__file__).parent / "images"
SIZE = (800, 800)

COLORS = [
    (255, 218, 233),
    (218, 238, 255),
    (255, 244, 218),
    (230, 255, 218),
    (238, 218, 255),
    (255, 230, 218),
    (218, 255, 244),
    (255, 218, 218),
]

ANIMALS = ["🐷", "🦫", "🐱", "🐻", "🐰", "🦊", "🐹", "🐨"]


def generate() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)

    try:
        font_large = ImageFont.truetype("arial.ttf", 120)
        font_small = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    for day in range(1, 68):
        days_left = 68 - day
        color = COLORS[day % len(COLORS)]
        animal = ANIMALS[day % len(ANIMALS)]

        img = Image.new("RGB", SIZE, color)
        draw = ImageDraw.Draw(img)

        draw.text((SIZE[0] // 2, SIZE[1] // 2 - 60), animal, font=font_large, anchor="mm")
        draw.text(
            (SIZE[0] // 2, SIZE[1] // 2 + 80),
            f"день {day:02d} · осталось {days_left}",
            fill=(80, 80, 80),
            font=font_small,
            anchor="mm",
        )

        img.save(IMAGES_DIR / f"day_{day:02d}.png")
        print(f"Создано: day_{day:02d}.png")


if __name__ == "__main__":
    generate()
