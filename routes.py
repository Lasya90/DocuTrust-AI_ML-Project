# app/api/routes.py

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import re

from app.ingestion.run_ingestion import ingest_pdf
from app.rag.store_instance import global_chunks
from app.rag.llm import generate_answer

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# 📤 UPLOAD PDF
# =========================
@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = ingest_pdf(file_path)

        return {
            "message": "PDF uploaded successfully",
            "chunks": result["chunks"]
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# REQUEST MODEL
# =========================
class QueryRequest(BaseModel):
    question: str


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


# =========================
# ASK API
# =========================
@router.post("/ask")
async def ask_question(req: QueryRequest):
    try:
        if not global_chunks:
            return {
                "question": req.question,
                "answer": "No PDF uploaded.",
                "source": ""
            }

        # 🔍 simple keyword search
        results = [
            chunk for chunk in global_chunks
            if req.question.lower() in chunk.lower()
        ]

        # fallback
        if not results:
            results = global_chunks[:3]

        context = " ".join(results[:3])

        answer = generate_answer(req.question, context)

        return {
            "question": req.question,
            "answer": answer,
            "source": results[0][:200]
        }

    except Exception as e:
        return {"error": str(e)}