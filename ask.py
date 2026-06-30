from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.vector_store import VectorStore

router = APIRouter()

store = VectorStore()

class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(req: AskRequest):

    results = store.search(req.question)

    if not results:
        return {
            "answer": "No relevant information found",
            "explanation": "",
            "source": ""
        }

    best = results[0]

    return {
        "answer": best["text"][:300],
        "explanation": f"Retrieved from most relevant section on page {best['page']}",
        "source": f"Page {best['page']}"
    }