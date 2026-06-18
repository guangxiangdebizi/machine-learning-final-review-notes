from __future__ import annotations

import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "PPT" / "PPT"
OUT_DIR = ROOT / "materials" / "extracted_text"


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    chunks: list[str] = []
    for page_index, page in enumerate(doc, start=1):
        text = normalize_text(page.get_text("text"))
        chunks.append(f"## Page {page_index}\n\n{text}\n")
    return "\n".join(chunks).strip() + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDFs found under: {PDF_DIR}")

    for pdf in pdfs:
        out_path = OUT_DIR / f"{pdf.stem}.txt"
        out_path.write_text(extract_pdf(pdf), encoding="utf-8")
        print(f"wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
