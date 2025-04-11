from pathlib import Path
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import os

input_folder = Path("model/files")
output_folder = Path("model/txt")
output_folder.mkdir(parents=True, exist_ok=True)

def convert_pdf_to_txt(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
        return ""

def convert_html_to_txt(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text()
    except Exception as e:
        print(f"Error reading {html_path}: {e}")
        return ""

for file_path in input_folder.glob("*"):
    if file_path.suffix.lower() == ".pdf":
        text = convert_pdf_to_txt(file_path)
    elif file_path.suffix.lower() == ".html":
        text = convert_html_to_txt(file_path)
    else:
        continue

    if text.strip():
        out_file = output_folder / f"{file_path.stem}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Saved: {out_file}")
