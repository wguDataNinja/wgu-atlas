#!/usr/bin/env python3
"""
extract_guide_texts.py
======================
Converts WGU program guide PDFs to plain text files using pdftotext.

One .txt produced per .pdf. Skips regeneration if .txt already exists
unless --force is passed.

Usage:
    WGU_GUIDES_PDF_DIR=/path/to/raw_pdfs \\
    WGU_GUIDES_TEXT_DIR=/path/to/raw_texts \\
    python3 scripts/program_guides/extract_guide_texts.py [--force]

Defaults:
    PDF dir:  ~/Desktop/WGU-Reddit/WGU_catalog/program_guides/raw_pdfs/
    Text dir: ~/Desktop/WGU-Reddit/WGU_catalog/program_guides/raw_texts/

Requires:
    pdftotext (Homebrew: brew install poppler)
"""

import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — configurable via environment variables
# ---------------------------------------------------------------------------
_HOME = Path.home()
_DEFAULT_PDF_DIR  = _HOME / "Desktop" / "WGU-Reddit" / "WGU_catalog" / "program_guides" / "raw_pdfs"
_DEFAULT_TEXT_DIR = _HOME / "Desktop" / "WGU-Reddit" / "WGU_catalog" / "program_guides" / "raw_texts"

PDF_DIR  = Path(os.environ.get("WGU_GUIDES_PDF_DIR",  str(_DEFAULT_PDF_DIR)))
TEXT_DIR = Path(os.environ.get("WGU_GUIDES_TEXT_DIR", str(_DEFAULT_TEXT_DIR)))

FORCE = "--force" in sys.argv


def _check_pdftotext():
    """Verify pdftotext is available on PATH."""
    result = subprocess.run(["which", "pdftotext"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: pdftotext not found. Install via: brew install poppler")
        sys.exit(1)


def extract_pdf(pdf_path: Path, txt_path: Path) -> bool:
    """
    Extract text from pdf_path → txt_path using pdftotext.
    Returns True on success, False on failure.
    pdftotext without -layout produces clean line-per-row text that matches
    the format of the already-extracted BSDA.txt reference file.
    """
    result = subprocess.run(
        ["pdftotext", str(pdf_path), str(txt_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def main():
    _check_pdftotext()

    if not PDF_DIR.exists():
        print(f"ERROR: PDF directory not found: {PDF_DIR}")
        sys.exit(1)

    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}")
        sys.exit(1)

    total     = len(pdfs)
    converted = 0
    skipped   = 0
    failed    = []

    print(f"PDF source:  {PDF_DIR}")
    print(f"Text output: {TEXT_DIR}")
    print(f"Total PDFs:  {total}")
    print(f"Force mode:  {FORCE}")
    print()

    for pdf_path in pdfs:
        txt_path = TEXT_DIR / (pdf_path.stem + ".txt")

        if txt_path.exists() and not FORCE:
            skipped += 1
            continue

        ok = extract_pdf(pdf_path, txt_path)
        if ok:
            converted += 1
            print(f"  OK  {pdf_path.name}")
        else:
            failed.append(pdf_path.name)
            print(f"  FAIL  {pdf_path.name}")

    print()
    print(f"=== Extraction summary ===")
    print(f"  Total:     {total}")
    print(f"  Converted: {converted}")
    print(f"  Skipped:   {skipped}  (already exist; use --force to re-extract)")
    print(f"  Failed:    {len(failed)}")
    if failed:
        for name in failed:
            print(f"    {name}")


if __name__ == "__main__":
    main()
