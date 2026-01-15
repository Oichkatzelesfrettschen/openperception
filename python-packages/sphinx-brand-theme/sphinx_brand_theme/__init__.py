from __future__ import annotations
from pathlib import Path

def get_html_theme_path() -> str:
    return str(Path(__file__).resolve().parent)

