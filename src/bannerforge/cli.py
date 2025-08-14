from __future__ import annotations

from typing import Annotated

import typer

from .renderer import generate_banner

__version__ = "0.2.0"

app = typer.Typer(
    add_completion=False,
    help="🎨 BannerForge - Generate stylish event banners with QR codes",
    rich_markup_mode="rich",
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"BannerForge v{__version__}")
        raise typer.Exit()


@app.command()  # type: ignore[misc]
def main(  # type: ignore[no-untyped-def]
    # Core required fields
    speaker: Annotated[str, typer.Option(help="Speaker name")] = ...,  # type: ignore[assignment]
    title: Annotated[str, typer.Option(help="Talk title")] = ...,  # type: ignore[assignment]
    date: Annotated[str, typer.Option(help="Date string")] = ...,  # type: ignore[assignment]
    venue: Annotated[str, typer.Option(help="Venue string")] = ...,  # type: ignore[assignment]
    # Optional media
    photo: Annotated[
        str | None, typer.Option(help="URL or path to speaker photo")
    ] = None,
    logo: Annotated[str | None, typer.Option(help="URL or path to logo")] = None,
    hashtag: Annotated[
        str | None, typer.Option(help="Hashtag or short tagline")
    ] = None,
    # Style options
    style: Annotated[str, typer.Option(help="Style preset")] = "arc",
    palette: Annotated[str, typer.Option(help="Color palette")] = "emerald",
    size: Annotated[str, typer.Option(help="Canvas size WxH")] = "1080x1080",
    # Output options
    output: Annotated[str, typer.Option(help="Output PNG path")] = "out/banner.png",
    pdf: Annotated[str | None, typer.Option(help="Optional PDF output path")] = None,
    # URLs
    site_url: Annotated[
        str | None, typer.Option(help="Site URL (default pythoncdmx.org)")
    ] = None,
    telegram_url: Annotated[
        str | None, typer.Option(help="Telegram URL (default t.me/PythonCDMX)")
    ] = None,
    # Palette extraction
    palette_from: Annotated[
        str | None, typer.Option(help="Image to extract palette from")
    ] = None,
    # QR options
    qr_data: Annotated[
        str | None, typer.Option(help="Data for QR (defaults to site_url)")
    ] = None,
    qr_ecc: Annotated[
        str, typer.Option(help="QR error correction level: L/M/Q/H")
    ] = "M",
    qr_scale: Annotated[int, typer.Option(help="QR scale (pixels per module)")] = 8,
    # Version
    _version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, help="Show version"),
    ] = None,
):
    """Generate an event banner with the specified parameters."""
    w, h = _parse_size(size)
    generate_banner(
        speaker_name=speaker,
        talk_title=title,
        date=date,
        venue=venue,
        photo=photo,
        logo=logo,
        hashtag=hashtag,
        style=style,
        palette=palette,
        size=(w, h),
        output=output,
        output_pdf=pdf,
        site_url=site_url,
        telegram_url=telegram_url,
        palette_from=palette_from,
        qr_data=qr_data,
        qr_ecc=qr_ecc,
        qr_scale=qr_scale,
    )
    typer.echo(f"Saved: {output}{' and ' + pdf if pdf else ''}")


def _parse_size(s: str) -> tuple[int, int]:
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except Exception:
        return 1600, 900


if __name__ == "__main__":
    app()
