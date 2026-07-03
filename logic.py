from models import PosePacket

def process_pose(packet: PosePacket):
    body = packet.body
    actions = []
    score = 0

    # Basic safety check
    if len(body) < 25:
        return {"error": "invalid body data"}

    # Example: squat detection (hip vs knee)
    try:
        hip_y = body[23].y
        knee_y = body[25].y

        if hip_y > knee_y:
            actions.append("standing")
        else:
            actions.append("squat")
            score += 10
    except:
        pass

    # Hand detection
    if packet.left_hand:
        actions.append("left_hand_active")
        score += 2

    if packet.right_hand:
        actions.append("right_hand_active")
        score += 2

    return {
        "user_id": packet.user_id,
        "actions": actions,
        "score": score
    }
