from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import ImageDraw, ImageFont

from .fonts import DEFAULT_TITLE_FONTS, safe_font


def auto_shrink_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_paths: str | list[str] | tuple[str, ...],
    max_width: int,
    max_font: int,
    min_font: int,
) -> tuple[ImageFont.FreeTypeFont, str]:
    """Auto-shrink text to fit within max_width."""
    for size in range(max_font, min_font - 1, -2):
        font = safe_font(font_paths, size)
        w = draw.textlength(text, font=font)
        if w <= max_width:
            return font, text
    font = safe_font(DEFAULT_TITLE_FONTS, min_font)
    wrapper = textwrap.TextWrapper(
        width=max(
            10, int(len(text) * max_width / max(1, draw.textlength(text, font=font)))
        )
    )
    wrapped = "\n".join(wrapper.wrap(text))
    return font, wrapped
