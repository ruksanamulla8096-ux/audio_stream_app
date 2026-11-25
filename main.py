import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Path to the frontend HTML file
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "../frontend/index.html")


@app.get("/")
async def get_client():
    with open(FRONTEND_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.websocket("/ws/audio")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    print("Client connected for audio streaming.")
    total_bytes = 0

    try:
        while True:
            # Receive binary audio chunk from the browser
            audio_chunk = await websocket.receive_bytes()
            chunk_size = len(audio_chunk)
            total_bytes += chunk_size

            # TODO: Pass `audio_chunk` to your STT engine (e.g., Whisper, Deepgram)
            # or save to a file/buffer here.
            print(f"Received chunk: {chunk_size} bytes | Total: {total_bytes} bytes")

            # Optional: Send acknowledgment or transcription back to client
            await websocket.send_text(f"Server received {total_bytes} bytes")

    except WebSocketDisconnect:
        print(f"Client disconnected. Total audio received: {total_bytes} bytes.")
    except Exception as e:
        print(f"WebSocket error: {e}")