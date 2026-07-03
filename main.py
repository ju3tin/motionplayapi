from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# -------------------------
# DATA STRUCTURE
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
    left_hand: Optional[List[Landmark]] = None
    right_hand: Optional[List[Landmark]] = None

# -------------------------
# SIMPLE GAME LOGIC
# -------------------------
def process(packet: PosePacket):
    actions = []
    score = 0

    # squat detection
    if len(packet.body) >= 26:
        hip = packet.body[23].y
        knee = packet.body[25].y

        if hip > knee:
            actions.append("standing")
        else:
            actions.append("squat")
            score += 10

    # hand detection
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
# HEALTH CHECK
# -------------------------
@app.get("/")
def home():
    return {"status": "MotionPlay running"}

# -------------------------
# WEBSOCKET
# -------------------------
@app.websocket("/pose")
async def pose_socket(ws: WebSocket):
    await ws.accept()

    while True:
        data = await ws.receive_json()
        packet = PosePacket(**data)

        result = process(packet)
        await ws.send_json(result)
