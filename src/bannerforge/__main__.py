"""Allow running bannerforge as a module with python -m bannerforge."""

from .cli import app

if __name__ == "__main__":
    app()
