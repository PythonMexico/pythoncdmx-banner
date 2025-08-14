from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PIL import Image

from .fonts import DEFAULT_TEXT_FONTS, DEFAULT_TITLE_FONTS


@dataclass
class Style:
    name: str
    bg: tuple[int, int, int]
    primary: tuple[int, int, int]
    secondary: tuple[int, int, int]
    accent: tuple[int, int, int]
    title_fonts: tuple[str, ...] = tuple(DEFAULT_TITLE_FONTS)
    text_fonts: tuple[str, ...] = tuple(DEFAULT_TEXT_FONTS)


def _quantize_palette(path: str, k: int = 6) -> list[tuple[int, int, int]]:
    img = Image.open(path).convert("RGB")
    pal = img.convert("P", palette=Image.ADAPTIVE, colors=k)
    palette_data = pal.getpalette()
    if palette_data is None:
        raise ValueError("Image has no palette")
    palette = palette_data[: k * 3]

    colors = [
        (palette[i], palette[i + 1], palette[i + 2]) for i in range(0, len(palette), 3)
    ]

    def lum(c: tuple) -> Any:
        r, g, b = [x / 255 for x in c]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    colors.sort(key=lum, reverse=True)
    return colors


PALETTES: dict[str, Style] = {
    "emerald": Style(
        "emerald",
        bg=(16, 24, 32),
        primary=(16, 185, 129),
        secondary=(209, 213, 219),
        accent=(99, 102, 241),
    ),
    "sunset": Style(
        "sunset",
        bg=(20, 20, 28),
        primary=(244, 114, 182),
        secondary=(253, 186, 116),
        accent=(59, 130, 246),
    ),
    "mono": Style(
        "mono",
        bg=(18, 18, 18),
        primary=(255, 255, 255),
        secondary=(156, 163, 175),
        accent=(99, 102, 241),
    ),
}


def palette_from_image(name: str, path: str) -> Style:
    colors = _quantize_palette(path, 6)
    primary = colors[0]
    accent = colors[1] if len(colors) > 1 else (99, 102, 241)
    bg = colors[-1] if len(colors) > 2 else (20, 20, 20)
    secondary = colors[2] if len(colors) > 2 else (209, 213, 219)
    return Style(name=name, bg=bg, primary=primary, secondary=secondary, accent=accent)
