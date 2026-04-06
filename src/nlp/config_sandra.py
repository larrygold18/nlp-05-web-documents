"""
config_sandra.py

Purpose

  Store configuration values for the EVTL pipeline.

Analytical Questions

- What web page should be used as the source?
- Where should raw HTML be saved?
- Where should processed tabular output be saved?

Notes

- This custom version uses Sandra-specific raw and processed file names.
- It prevents overwriting the original case files.
"""

from pathlib import Path

# ============================================================
# WEB CONFIGURATION
# ============================================================

WEB_URL: str = "https://arxiv.org/abs/2602.20021"

HTTP_REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": "sandra-html-text-project/1.0",
    "Accept": "text/html",
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

RAW_HTML_PATH: Path = RAW_PATH / "sandra_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "sandra_processed.csv"
