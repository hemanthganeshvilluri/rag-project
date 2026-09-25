from fastapi import APIRouter, Request
from pydantic import BaseModel
from query_pipeline import query_pipeline

router = APIRouter()

class Chatrequest(BaseModel):
    query: str

@router.post('/chat')
async def chat(req: Request, chat_req: Chatrequest):
    models = req.app.state.models
    vector_db = req.app.state.vector_db

    query, response, chunks = query_pipeline(query, vector_db, models)
    return {
        "query": query,
        "answer": response,
        "sources": [
            {
                "source": chunk.metadata["source"],
                "type": chunk.metadata["type"],
                "section": chunk.metadata["section"],
                "page_no": chunk.metadata["page_no"]
            }
            for chunk in chunks
        ]
    }
