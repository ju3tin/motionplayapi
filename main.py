from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# -------------------------
# DATA MODEL
# -------------------------
class Landmark(BaseModel):
    x: float
    y: float
    z: float = 0.0
    visibility: Optional[float] = None

class PosePacket(BaseModel):
    user_id: str
    timestamp: int
    body: List[Landmark]
    left_hand: Optional[list] = None
    right_hand: Optional[list] = None

# -------------------------
# SIMPLE GAME LOGIC
# -------------------------
def process_pose(packet: PosePacket):
    if len(packet.body) < 25:
        return {"error": "invalid pose"}

    actions = []
    score = 0

    try:
        hip = packet.body[23].y
        knee = packet.body[25].y

        if hip > knee:
            actions.append("standing")
        else:
            actions.append("squat")
            score += 10
    except:
        pass

    if packet.left_hand:
        actions.append("left_hand")
        score += 2

    if packet.right_hand:
        actions.append("right_hand")
        score += 2

    return {
        "user_id": packet.user_id,
        "actions": actions,
        "score": score
    }

# -------------------------
# HTTP TEST ROUTE
# -------------------------
@app.get("/")
def home():
    return {"status": "MotionPlay API running"}

# -------------------------
# WEBSOCKET ROUTE
# -------------------------
@app.websocket("/pose")
async def pose_socket(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            packet = PosePacket(**data)

            result = process_pose(packet)

            await websocket.send_json(result)

        except Exception as e:
            await websocket.send_json({"error": str(e)})
