from fastapi import APIRouter, UploadFile, File
import os, shutil

from app.ingestion.pdf_loader import parse_pdf_to_chunks
from app.rag.vector_store import VectorStore

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

store = VectorStore()   # 🔥 global memory

@router.post("/upload-and-process")
async def upload_and_process(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = parse_pdf_to_chunks(file_path)

    store.add(chunks)

    return {
        "message": "File processed",
        "chunks": len(chunks)
    }