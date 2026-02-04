from fastapi import APIRouter, WebSocket
import ollama

from app.rag.retrieval import query_docs

router = APIRouter()

@router.websocket("/ws")
async def chat_ws(ws: WebSocket):
    await ws.accept()

    while True:
        prompt = await ws.receive_text()

        docs = query_docs(prompt, k=4)
        if not docs:
            await ws.send_text("I don't know. I couldn't find anything in the docs.")
            continue

        context = "\n\n".join(docs)
        system = (
            "You are a helpful assistant. Answer using the provided context. "
            "If the answer is not in the context, say you don't know."
        )

        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"},
            ],
            stream=True,
        )

        for chunk in response:
            if "message" in chunk:
                await ws.send_text(chunk["message"]["content"])
