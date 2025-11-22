import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe('driver-updates')

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = message['data']
                await websocket.send_text(data)
            await asyncio.sleep(0.01) # Prevent tight loop
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await pubsub.unsubscribe('driver-updates')
        await r.close()

@app.get("/")
def read_root():
    return {"message": "Cab Location Tracker API is running"}
