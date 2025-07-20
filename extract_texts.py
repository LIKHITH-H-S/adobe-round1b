import os
from PyPDF2 import PdfReader

# Input and output folders
pdf_dir = "datasets/pdfs"
text_dir = "datasets/texts"
os.makedirs(text_dir, exist_ok=True)

# Loop over all PDF files
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        text_path = os.path.join(text_dir, filename.replace(".pdf", ".txt"))

        try:
            print(f"Extracting: {filename}")
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            print(f"❌ Failed to extract {filename}: {e}")

print("✅ All PDF files converted to text.")
