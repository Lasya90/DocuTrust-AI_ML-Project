from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.rag.crag_graph import run_crag_pipeline
from app.database import traces_collection  # FIXED
import asyncio

router = APIRouter(prefix="/api/query", tags=["query"])


@router.websocket("/ws")
async def query_websocket(websocket: WebSocket):
    """
    Streams CRAG pipeline steps in real time and returns final answer with citations.
    """
    await websocket.accept()

    try:
        while True:
            payload = await websocket.receive_json()

            client_id = payload.get("client_id")
            query = payload.get("query")
            doc_id = payload.get("doc_id")

            if not query:
                await websocket.send_json({
                    "type": "error",
                    "message": "Query is required"
                })
                continue

            # Run pipeline in thread (non-blocking)
            loop = asyncio.get_event_loop()
            final_state = await loop.run_in_executor(
                None,
                run_crag_pipeline,
                query,
                doc_id
            )

            # Stream trace steps
            for step in final_state.get("trace", []):
                await websocket.send_json({
                    "type": "trace_step",
                    "data": step
                })
                await asyncio.sleep(0.15)

            # Build citations safely
            citations = []
            for c in final_state.get("final_context", []):
                citations.append({
                    "chunk_id": c.get("chunk_id"),
                    "page": c.get("metadata", {}).get("page_number"),
                    "source": c.get("metadata", {}).get("source", "document")
                })

            # Send final answer
            await websocket.send_json({
                "type": "final_answer",
                "data": {
                    "answer": final_state.get("answer"),
                    "citations": citations,
                    "used_web_fallback": final_state.get("used_web_fallback", False),
                    "citation_check": final_state.get("citation_check", None),
                }
            })

            # Save trace (NO Pydantic model dependency)
            trace_record = {
                "client_id": client_id,
                "query": query,
                "steps": final_state.get("trace", []),
                "final_answer": final_state.get("answer"),
                "citations": citations,
                "used_web_fallback": final_state.get("used_web_fallback", False),
            }

            await traces_collection.insert_one(trace_record)

    except WebSocketDisconnect:
        pass