from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
import pdfplumber

from app.rag.vector_store import VectorStore
from app.rag.retriever import retrieve

app = FastAPI()

# 🔥 SINGLE SHARED STORE
vector_store = VectorStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PDF → chunks
def extract_pdf(file_bytes):
    chunks = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                chunks.append({
                    "text": text,
                    "source": f"Page {i+1}"
                })

    return chunks


@app.get("/")
def home():
    return {"msg": "DocuTrust Running 🚀"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()

    chunks = extract_pdf(content)

    vector_store.add_text(chunks)

    return {
        "message": "PDF uploaded",
        "chunks": len(chunks)
    }


class Question(BaseModel):
    question: str


@app.post("/ask")
async def ask(q: Question):
    return retrieve(q.question, vector_store)