---
```markdown
# Video Processing Pipeline

This is a distributed event-driven video processing pipeline built with **FastAPI**, **RabbitMQ**, and **Python**. The system allows users to upload videos, enhance them (e.g., adjust colors, FPS), and extract metadata (e.g., duration, resolution).

---

## Features
- **Video Upload**: Users can upload videos via HTTP.
- **Video Enhancement**: Videos are enhanced using simple adjustments (e.g., color correction, FPS changes).
- **Metadata Extraction**: Basic metadata (e.g., duration, resolution) is extracted from the video.
- **Real-Time Updates**: Users receive real-time updates via WebSocket connections.

---

## Technologies Used
- **FastAPI**: For handling HTTP requests, WebSocket connections, and communication between clients and workers.
- **RabbitMQ**: For task distribution between workers.
- **MoviePy**: For video enhancement and metadata extraction.
- **React** (optional): For a basic client interface (not included in this repository).

---

## How to Run the Project

### Prerequisites
1. **Python 3.8+**: Install Python from [python.org](https://www.python.org/).
2. **RabbitMQ**: Install RabbitMQ from [rabbitmq.com](https://www.rabbitmq.com/).
3. **Git**: Install Git from [git-scm.com](https://git-scm.com/).

---

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/video-processing-pipeline.git
cd video-processing-pipeline
```

---

### Step 2: Set Up the Virtual Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

---

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

### Step 4: Start RabbitMQ
1. Start the RabbitMQ server. On most systems, you can run:
   ```bash
   rabbitmq-server
   ```
2. Ensure RabbitMQ is running on `localhost:5672`.

---

### Step 5: Run the FastAPI Server
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. The server will run at `http://localhost:8000`.

---

### Step 6: Run the Workers
1. Open a new terminal window and activate the virtual environment (as in Step 2).
2. Run the **Video Enhancement Worker**:
   ```bash
   python video_enhancement_worker.py
   ```
3. Open another terminal window and run the **Metadata Extraction Worker**:
   ```bash
   python metadata_extraction_worker.py
   ```

---

### Step 7: Test the System
1. Use **Postman** or **curl** to upload a video:
   ```bash
   curl -X POST -F "file=@your_video.mp4" http://localhost:8000/upload
   ```
2. Check the terminal logs of the workers to see the video being processed.
3. Use a WebSocket client to connect to `ws://localhost:8000/ws` and receive real-time updates.

---

## Contributing
Contributions are welcome! If you find any issues or want to add new features, feel free to open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
