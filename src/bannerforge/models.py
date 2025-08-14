from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    speaker: str
    title: str
    date: str
    venue: str
    photo: str | None = None
    logo: str | None = None
    hashtag: str | None = None
    style: str = Field(
        default="arc", pattern="^(gradient|split|card|arc|pill-left|glass)$"
    )
    palette: str = Field(default="emerald")
    size: str = Field(default="1080x1080")

    # QR
    qr_data: str | None = None  # if None -> uses site_url default
    qr_ecc: str = Field(default="M", pattern="^[LMQH]$")
    qr_scale: int = Field(default=8, ge=1, le=30)

    # Links / palette
    site_url: str | None = None  # default set in renderer
    telegram_url: str | None = None  # default set in renderer
    palette_from: str | None = None
