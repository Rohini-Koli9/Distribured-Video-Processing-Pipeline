from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import pika
import uuid

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='video_tasks', exchange_type='fanout')

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Publish task to RabbitMQ
    channel.basic_publish(exchange='video_tasks', routing_key='', body=file_id)
    
    return JSONResponse(content={"file_id": file_id})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@app.post("/internal/video-enhancement-status")
async def video_enhancement_status(file_id: str, status: str):
    # Handle status update
    return {"status": "received"}

@app.post("/internal/metadata-extraction-status")
async def metadata_extraction_status(file_id: str, status: str):
    # Handle status update
    return {"status": "received"}