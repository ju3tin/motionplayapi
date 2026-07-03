from fastapi import FastAPI, WebSocket
from models import PosePacket
from logic import process_pose
import json

app = FastAPI()

@app.get("/")
def health():
    return {"status": "MotionPlay API running"}

@app.websocket("/pose")
async def pose_socket(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_text()

            packet = PosePacket.model_validate_json(data)
            result = process_pose(packet)

            await websocket.send_json(result)

        except Exception as e:
            await websocket.send_json({
                "error": str(e)
            })
