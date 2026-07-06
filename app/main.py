import base64

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.face_detect import decode_frame, detect

app = FastAPI(title="MIMETA Face Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # lista resuelta por ambiente (dev/stg/prod)
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.websocket("/ws/face-detect")
async def face_detect_ws(ws: WebSocket):
    await ws.accept()
    try:
        async for message in ws.iter_text():
            # El cliente envía data-URL: "data:image/jpeg;base64,<datos>"
            raw = message.split(",", 1)[-1]
            jpeg_bytes = base64.b64decode(raw)

            frame = decode_frame(jpeg_bytes)
            if frame is None:
                await ws.send_json({"face_detected": False, "confidence": 0.0, "bbox": None})
                continue

            result = detect(frame)
            await ws.send_json(result)

    except WebSocketDisconnect:
        pass
