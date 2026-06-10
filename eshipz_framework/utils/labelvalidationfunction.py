import re
from pathlib import Path
import openpyxl
from PyPDF2 import PdfReader


# ---------------- TEXT NORMALIZATION ---------------- #

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------- EXCEL DATA EXTRACTION ---------------- #

def extract_excel_text(excel_path: Path) -> list[str]:
    wb = openpyxl.load_workbook(excel_path)
    sh = wb["bulk_upload"]

    values = set()

    for row in sh.iter_rows(min_row=2):
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                cleaned = normalize_text(cell.value)
                if len(cleaned) > 2:   # ignore noise
                    values.add(cleaned)

    return list(values)


# ---------------- PDF DATA EXTRACTION ---------------- #

def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return normalize_text(text)