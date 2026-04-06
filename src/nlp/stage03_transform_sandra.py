"""
stage03_transform_sandra.py

Source: BeautifulSoup object
Sink: Pandas DataFrame

Purpose

  Transform validated HTML into a structured tabular format.

Analytical Questions

- Which fields should be extracted from the web page?
- How can the HTML be normalized into a clean record?
- What derived values would make the data more useful?

Notes

- This custom version extracts more metadata from the arXiv page.
- It adds derived metrics such as author_count and abstract_length.
- It creates a richer output than the original case version.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup
import pandas as pd

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform validated HTML into a structured DataFrame."""

    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    # ============================================================
    # EXTRACT TITLE
    # ============================================================

    title_tag = soup.find("h1", class_="title")
    title = title_tag.get_text(strip=True) if title_tag is not None else "unknown"
    title = title.replace("Title:", "").strip()

    # ============================================================
    # EXTRACT AUTHORS
    # ============================================================

    authors_tag = soup.find("div", class_="authors")
    author_tags_list = authors_tag.find_all("a") if authors_tag is not None else []
    authors = ", ".join([tag.get_text(strip=True) for tag in author_tags_list])
    author_count = len(author_tags_list)

    # ============================================================
    # EXTRACT ABSTRACT
    # ============================================================

    abstract_tag = soup.find("blockquote", class_="abstract")
    abstract = (
        abstract_tag.get_text(strip=True).replace("Abstract:", "").strip()
        if abstract_tag is not None
        else "unknown"
    )
    abstract_length = len(abstract)

    # ============================================================
    # EXTRACT SUBJECTS
    # ============================================================

    subjects_tag = soup.find("td", class_="tablecell subjects")
    subjects = (
        subjects_tag.get_text(" ", strip=True)
        if subjects_tag is not None
        else "unknown"
    )

    # ============================================================
    # EXTRACT SUBMISSION DATE
    # ============================================================

    dateline_tag = soup.find("div", class_="dateline")
    submitted_date = (
        dateline_tag.get_text(strip=True) if dateline_tag is not None else "unknown"
    )

    # ============================================================
    # EXTRACT DOI
    # ============================================================

    doi_tag = soup.find("a", id="arxiv-doi-link")
    doi = doi_tag.get_text(strip=True) if doi_tag is not None else "unknown"

    # ============================================================
    # EXTRACT PDF LINK
    # ============================================================

    pdf_tag = soup.find("a", class_="abs-button download-pdf")
    pdf_url = (
        pdf_tag["href"]
        if pdf_tag is not None and pdf_tag.has_attr("href")
        else "unknown"
    )

    if pdf_url.startswith("/"):
        pdf_url = f"https://arxiv.org{pdf_url}"

    # ============================================================
    # ADD CUSTOM ANALYTICAL FEATURES
    # ============================================================

    if author_count <= 3:
        author_team_size = "small"
    elif author_count <= 10:
        author_team_size = "medium"
    else:
        author_team_size = "large"

    if abstract_length < 500:
        abstract_size_label = "short"
    elif abstract_length < 1200:
        abstract_size_label = "medium"
    else:
        abstract_size_label = "long"

    has_doi = "yes" if doi != "unknown" else "no"

    submitted_text = submitted_date.lower()
    paper_age_label = "recent" if "2026" in submitted_text else "older"

    # ============================================================
    # CREATE RECORD
    # ============================================================

    record = {
        "title": title,
        "authors": authors,
        "author_count": author_count,
        "author_team_size": author_team_size,
        "abstract": abstract,
        "abstract_length": abstract_length,
        "abstract_size_label": abstract_size_label,
        "subjects": subjects,
        "submitted_date": submitted_date,
        "paper_age_label": paper_age_label,
        "doi": doi,
        "has_doi": has_doi,
        "pdf_url": pdf_url,
    }

    # ============================================================
    # CREATE DATAFRAME
    # ============================================================

    df = pd.DataFrame([record])

    # ============================================================
    # LOG RESULTS
    # ============================================================

    LOG.info(f"Author team size: {author_team_size}")
    LOG.info(f"Abstract size label: {abstract_size_label}")
    LOG.info(f"Has DOI: {has_doi}")
    LOG.info(f"Paper age label: {paper_age_label}")

    LOG.info("Transformation complete.")
    LOG.info(f"Columns: {list(df.columns)}")
    LOG.info(f"DataFrame preview:\n{df.head()}")
    LOG.info("Sink: Pandas DataFrame created")

    return df
