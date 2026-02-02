


from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        stream = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": request.prompt}],
            stream=True,
        )

        for chunk in stream:
            if "message" in chunk:
                yield chunk["message"]["content"]

    return StreamingResponse(generate(), media_type="text/plain")


# .\.venv\Scripts\Activate.ps1