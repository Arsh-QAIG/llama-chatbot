from fastapi import APIRouter, WebSocket
import ollama

router = APIRouter()

@router.websocket("/ws")
async def chat_ws(ws: WebSocket):
    await ws.accept()

    while True:
        prompt = await ws.receive_text()

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        for chunk in response:
            await ws.send_text(chunk["message"]["content"])
