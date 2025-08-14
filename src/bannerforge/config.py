from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
CACHE_DIR = os.getenv("BANNERFORGE_CACHE", ".cache")
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
DEFAULT_SITE = "pythoncdmx.org"
DEFAULT_TELEGRAM = "https://t.me/PythonCDMX"
