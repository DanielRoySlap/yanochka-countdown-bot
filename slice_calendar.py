"""Нарезка календаря-сетки на отдельные картинки day_01.png … day_67.png."""

from pathlib import Path

from PIL import Image

SOURCE = Path(__file__).parent / "source_calendar.png"
OUTPUT = Path(__file__).parent / "images"

# Границы ячеек (из анализа отступов между карточками)
COLS = [0, 128, 256, 384, 512, 640, 768, 896, 1024]
ROWS = [0, 120, 240, 360, 480, 588, 690, 784, 870, 949, 1024]

# (row, col, день на карточке) — порядок сверху вниз, слева направо
TILES: list[tuple[int, int, int]] = [
    # row 0
    (0, 0, 67), (0, 1, 66), (0, 2, 65), (0, 3, 64), (0, 4, 63), (0, 5, 62), (0, 6, 61),
    # row 1
    (1, 0, 60), (1, 1, 59), (1, 2, 58), (1, 3, 57), (1, 4, 56), (1, 5, 55), (1, 7, 54),
    # row 2
    (2, 0, 53), (2, 1, 52), (2, 2, 51), (2, 3, 50), (2, 4, 49), (2, 5, 48), (2, 7, 47),
    # row 3
    (3, 0, 46), (3, 1, 45), (3, 2, 44), (3, 3, 43), (3, 4, 42), (3, 5, 41), (3, 7, 40),
    # row 4
    (4, 0, 39), (4, 1, 38), (4, 2, 37), (4, 3, 36), (4, 4, 35), (4, 5, 34), (4, 6, 33),
    # row 5
    (5, 0, 32), (5, 1, 31), (5, 2, 30), (5, 3, 29), (5, 4, 28), (5, 5, 27), (5, 7, 26),
    # row 6
    (6, 0, 25), (6, 1, 24), (6, 2, 23), (6, 3, 22), (6, 4, 21), (6, 5, 20), (6, 7, 19),
    # row 7
    (7, 0, 18), (7, 1, 17), (7, 2, 16), (7, 3, 15), (7, 4, 14), (7, 5, 13), (7, 6, 12),
    # row 8
    (8, 0, 11), (8, 1, 10), (8, 2, 9), (8, 3, 8), (8, 4, 7), (8, 5, 6),
    # row 9
    (9, 0, 4), (9, 1, 3), (9, 2, 2), (9, 3, 1),
]

# День 5 отсутствует на сетке — дублируем соседнюю карточку (6 дней)
MISSING_DAY_FALLBACK = 6

# Финальная большая картинка — правая нижняя часть сетки
FINAL_BOX = (COLS[6], ROWS[8], COLS[8], ROWS[10])


def crop_cell(img: Image.Image, row: int, col: int) -> Image.Image:
    left, top = COLS[col], ROWS[row]
    right, bottom = COLS[col + 1], ROWS[row + 1]
    return img.crop((left, top, right, bottom))


def day_to_filename(day_on_card: int) -> str:
    return f"day_{68 - day_on_card:02d}.png"


def slice_calendar(source: Path = SOURCE, output: Path = OUTPUT) -> None:
    output.mkdir(exist_ok=True)
    img = Image.open(source).convert("RGB")

    saved: dict[int, Path] = {}

    for row, col, day in TILES:
        tile = crop_cell(img, row, col)
        filename = day_to_filename(day)
        path = output / filename
        tile.save(path, "PNG")
        saved[day] = path
        print(f"  {filename} <- card {day} (row {row}, col {col})")

    # День 5 → day_63.png
    fallback = saved[MISSING_DAY_FALLBACK]
    day63 = output / day_to_filename(MISSING_DAY_FALLBACK - 1)
    Image.open(fallback).save(day63, "PNG")
    print(f"  {day63.name} <- day 5 (copy from card {MISSING_DAY_FALLBACK})")

    # Большая финальная картинка → day_67.png (последний день)
    final = img.crop(FINAL_BOX)
    final_path = output / "day_67.png"
    final.save(final_path, "PNG")
    print("  day_67.png <- final welcome image")

    print(f"\nГотово: {len(list(output.glob('day_*.png')))} файлов в {output}")


if __name__ == "__main__":
    slice_calendar()
