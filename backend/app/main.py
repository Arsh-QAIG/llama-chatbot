from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import logging

from app.rag.retrieval import query_docs
from app.rag.index import index_docs
from app.api.websocket import router as ws_router

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()

logger = logging.getLogger("app")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)

@app.on_event("startup")
def startup():
    index_docs()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        try:
            docs = query_docs(request.prompt, k=4)
        except Exception as exc:
            logger.exception("Failed to retrieve docs")
            yield f"Error retrieving docs: {exc}"
            return

        if not docs:
            yield "I don't know. I couldn't find anything in the docs."
            return

        context = "\n\n".join(docs)
        system = (
            "You are a helpful assistant. Answer using the provided context. "
            "If the answer is not in the context, say you don't know."
        )

        try:
            stream = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.prompt}"},
                ],
                stream=True,
                options={"num_predict": 256, "num_ctx": 2048},
            )
        except Exception as exc:
            logger.exception("Model call failed")
            yield f"Error calling model: {exc}"
            return

        for chunk in stream:
            if "message" in chunk:
                yield chunk["message"]["content"]

    return StreamingResponse(generate(), media_type="text/plain")
