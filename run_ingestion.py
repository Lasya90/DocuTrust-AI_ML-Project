# app/ingestion/run_ingestion.py

import fitz
import re
from app.rag.store_instance import global_chunks


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return clean_text(text)


# =========================
# CHUNK TEXT
# =========================
def chunk_text(text, size=200):   # smaller = safer
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


# =========================
# INGEST PDF
# =========================
def ingest_pdf(pdf_path: str):
    text = extract_text(pdf_path)
    chunks = chunk_text(text)

    # ✅ STORE IN MEMORY
    global global_chunks
    global_chunks.clear()
    global_chunks.extend(chunks)

    print("✅ Stored chunks:", len(global_chunks))

    return {
        "status": "success",
        "chunks": len(chunks)
    }