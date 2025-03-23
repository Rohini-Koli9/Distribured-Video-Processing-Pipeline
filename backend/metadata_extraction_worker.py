# import pika
# import os
# from moviepy.editor import VideoFileClip

# UPLOAD_DIR = "uploads"

# def extract_metadata(file_id):
#     file_path = os.path.join(UPLOAD_DIR, file_id)
#     clip = VideoFileClip(file_path)
#     metadata = {
#         "duration": clip.duration,
#         "fps": clip.fps,
#         "size": clip.size
#     }
#     return metadata

# def callback(ch, method, properties, body):
#     file_id = body.decode()
#     metadata = extract_metadata(file_id)
#     print(f"Extracted metadata: {metadata}")
#     # Send status update to FastAPI server
#     # Implement this part using requests or another method

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.exchange_declare(exchange='video_tasks', exchange_type='fanout')

# result = channel.queue_declare(queue='', exclusive=True)
# queue_name = result.method.queue
# channel.queue_bind(exchange='video_tasks', queue=queue_name)

# channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()



import pika
import os
#import requests
from moviepy.editor import VideoFileClip

UPLOAD_DIR = "uploads"
FASTAPI_SERVER_URL = "http://127.0.0.1:8000/"  # Update this with your FastAPI server URL

def extract_metadata(file_id):
    file_path = os.path.join(UPLOAD_DIR, file_id)
    clip = VideoFileClip(file_path)
    metadata = {
        "duration": clip.duration,
        "fps": clip.fps,
        "size": clip.size
    }
    return metadata

def send_status_update(file_id, metadata):
    url = f"{FASTAPI_SERVER_URL}/status_update"
    payload = {
        "file_id": file_id,
        "metadata": metadata
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Status update sent successfully for file {file_id}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send status update for file {file_id}: {e}")

def callback(ch, method, properties, body):
    file_id = body.decode()
    metadata = extract_metadata(file_id)
    print(f"Extracted metadata: {metadata}")
    send_status_update(file_id, metadata)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='video_tasks', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='video_tasks', queue=queue_name)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()