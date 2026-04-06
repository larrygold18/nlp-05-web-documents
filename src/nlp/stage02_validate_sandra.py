"""
stage02_validate_sandra.py

Source: raw HTML string
Sink: BeautifulSoup object

Purpose

  Inspect HTML structure and validate that the page is usable.

Analytical Questions

- Does the HTML contain the required paper fields?
- Are the expected tags present?
- Is the page ready for transformation?

Notes

- This custom version checks for key arXiv fields before transformation.
- It improves reliability by failing early if required tags are missing.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_text: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure."""

    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    soup = BeautifulSoup(html_text, "html.parser")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    title_tag = soup.find("h1", class_="title")
    authors_tag = soup.find("div", class_="authors")
    abstract_tag = soup.find("blockquote", class_="abstract")
    subjects_tag = soup.find("td", class_="tablecell subjects")

    LOG.info(f"title_tag found: {title_tag is not None}")
    LOG.info(f"authors_tag found: {authors_tag is not None}")
    LOG.info(f"abstract_tag found: {abstract_tag is not None}")
    LOG.info(f"subjects_tag found: {subjects_tag is not None}")

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    if title_tag is None:
        raise ValueError("Expected title tag was not found.")

    if authors_tag is None:
        raise ValueError("Expected authors tag was not found.")

    if abstract_tag is None:
        raise ValueError("Expected abstract tag was not found.")

    LOG.info("Validation passed.")
    LOG.info("Sink: validated BeautifulSoup object")

    return soup
