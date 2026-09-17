import os
import fitz  # PyMuPDF
from pathlib import Path

source_dir = Path(r"c:\REP-ANTIGRAVITY\temp_extract")
output_dir = Path(r"c:\REP-ANTIGRAVITY\temp_extract\texts")
output_dir.mkdir(parents=True, exist_ok=True)

for file in source_dir.rglob("*.pdf"):
    print(f"Processing: {file.name}")
    try:
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        
        output_file = output_dir / f"{file.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved to: {output_file.name}")
    except Exception as e:
        print(f"Error processing {file.name}: {e}")
