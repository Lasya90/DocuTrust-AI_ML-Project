from typing import List, Dict, Any

class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    def get_answer(self, query: str, top_k: int = 3, threshold: float = 0.65) -> Dict[str, Any]:
        """
        1. Retrieve relevant chunks
        2. Apply similarity threshold
        3. If no good match → return NO RESULT
        """

        results = self.vector_store.similarity_search_with_score(query, k=top_k)

        if not results:
            return {
                "answer": "No relevant information found in uploaded document.",
                "sources": []
            }

        # filter by threshold
        filtered_chunks = []
        sources = []

        for doc, score in results:
            # lower score = better (FAISS depends on setup)
            if score >= threshold:
                continue

            filtered_chunks.append(doc.page_content)
            sources.append(doc.metadata.get("source", "PDF"))

        # ❌ IMPORTANT: no valid match
        if len(filtered_chunks) == 0:
            return {
                "answer": "No relevant information found in uploaded document.",
                "sources": []
            }

        # build context
        context = "\n\n".join(filtered_chunks)

        prompt = f"""
        Answer ONLY using the context below.
        If context is not enough, say "Not found in document".

        Context:
        {context}

        Question:
        {query}
        """

        answer = self.llm.invoke(prompt)

        return {
            "answer": answer,
            "sources": list(set(sources))  # remove duplicates
        }