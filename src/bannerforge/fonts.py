from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from PIL.ImageFont import FreeTypeFont

from PIL import ImageFont as _ImageFont

# CommitMono Nerd Font primary (override with assets/fonts)
DEFAULT_TITLE_FONTS = [
    "assets/fonts/CommitMono/CommitMonoNerdFontMono-Regular.otf",
    "assets/fonts/CommitMono/CommitMonoNerdFont-Bold.otf",
    "assets/fonts/CommitMono/CommitMonoNerdFontMono-Bold.otf",
    "assets/fonts/DejaVuSans/DejaVuSans.ttf",
    "assets/fonts/DejaVuSans/DejaVuSans-Bold.ttf",
]
DEFAULT_TEXT_FONTS = [
    "assets/fonts/CommitMono/CommitMonoNerdFontMono-Regular.otf",
    "assets/fonts/CommitMono/CommitMonoNerdFont-Bold.otf",
    "assets/fonts/CommitMono/CommitMonoNerdFont-Regular.otf",
    "assets/fonts/DejaVuSans/DejaVuSans-Bold.ttf",
    "assets/fonts/DejaVuSans/DejaVuSans.ttf",
]

ASSET_FONT_DIR = Path(__file__).parent.parent.parent / "assets" / "fonts"


def safe_font(paths: str | list[str] | tuple[str, ...], size: int) -> FreeTypeFont:
    """Load a font safely with fallbacks."""
    candidates: list[str] = []
    if isinstance(paths, list | tuple):
        candidates.extend(paths)
    elif isinstance(paths, str):
        candidates.append(paths)

    # Asset fonts (project-level override)
    if ASSET_FONT_DIR.is_dir():
        for font_file in ASSET_FONT_DIR.iterdir():
            if font_file.suffix.lower() == ".ttf":
                font_path = str(font_file)
                if "bold" in font_file.name.lower():
                    candidates.insert(0, font_path)
                else:
                    candidates.append(font_path)

    # System fallbacks
    candidates += [
        "assets/fonts/DejaVuSans/DejaVuSans-Bold.ttf",
        "assets/fonts/DejaVuSans/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]

    for font_path in candidates + list(
        paths if isinstance(paths, list | tuple) else [paths]
    ):
        try:
            if isinstance(font_path, str) and Path(font_path).exists():
                return _ImageFont.truetype(font_path, size=size)
        except OSError as err:  # Font loading errors
            raise RuntimeError(
                "Cannot load any TrueType font. Make sure at least one TrueType font exists."
            ) from err
    return cast("FreeTypeFont", _ImageFont.load_default())
