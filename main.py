from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import json
from datetime import datetime
import asyncio

app = FastAPI(title="MotionPlay Backend")

# Store connected clients
connected_clients = {}

@app.get("/")
async def get_root():
    return {"status": "MotionPlay Backend is running"}

@app.websocket("/pose")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = None
    
    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            
            client_id = packet.get("user_id", "unknown")
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Store latest data
            connected_clients[client_id] = {
                "data": packet,
                "last_seen": timestamp
            }
            
            # Echo back confirmation
            await websocket.send_json({
                "status": "received",
                "user_id": client_id,
                "timestamp": timestamp,
                "landmarks_count": len(packet.get("body", []))
            })
            
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]

@app.get("/clients")
async def get_clients():
    return {
        "connected": len(connected_clients),
        "clients": list(connected_clients.keys())
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
