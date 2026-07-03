from pydantic import BaseModel
from typing import List, Optional

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
