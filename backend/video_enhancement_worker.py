# import pika
# import os
# from moviepy import VideoFileClip

# UPLOAD_DIR = "uploads"

# def enhance_video(file_id):
#     file_path = os.path.join(UPLOAD_DIR, file_id)
#     output_path = os.path.join(UPLOAD_DIR, f"enhanced_{file_id}")
    
#     clip = VideoFileClip(file_path)
#     # Simple enhancement: increase brightness
#     enhanced_clip = clip.fx(lambda x: x * 1.2)
#     enhanced_clip.write_videofile(output_path, codec='libx264')
    
#     return output_path

# def callback(ch, method, properties, body):
#     file_id = body.decode()
#     enhanced_path = enhance_video(file_id)
#     print(f"Enhanced video saved to {enhanced_path}")
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
from moviepy.editor import VideoFileClip  

UPLOAD_DIR = "uploads"

def enhance_video(file_id):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_id)
        output_path = os.path.join(UPLOAD_DIR, f"enhanced_{file_id}")
        
        print(f"Processing video: {file_path}")
        print(f"Saving enhanced video to: {output_path}")
        
        clip = VideoFileClip(file_path)
        print("Video loaded successfully")
        
        # Simple enhancement: increase brightness
        enhanced_clip = clip.fx(lambda x: x * 1.2)
        print("Video enhanced successfully")
        
        enhanced_clip.write_videofile(output_path, codec='libx264')
        print("Enhanced video saved successfully")
        
        return output_path
    except Exception as e:
        print(f"Error enhancing video: {e}")
        return None

def callback(ch, method, properties, body):
    file_id = body.decode()
    enhanced_path = enhance_video(file_id)
    if enhanced_path:
        print(f"Enhanced video saved to {enhanced_path}")
    else:
        print(f"Failed to enhance video: {file_id}")

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='video_tasks', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='video_tasks', queue=queue_name)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()