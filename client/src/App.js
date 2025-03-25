import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [metadata, setMetadata] = useState(null);
  const [enhancedVideoUrl, setEnhancedVideoUrl] = useState('');

  // WebSocket connection for real-time updates
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'status') {
        setStatus(data.message);
      } else if (data.type === 'metadata') {
        setMetadata(data.metadata);
      } else if (data.type === 'enhanced_video') {
        setEnhancedVideoUrl(data.url);
      }
    };

    return () => ws.close();
  }, []);

  // Handle file upload
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setStatus(`File uploaded successfully: ${response.data.file_id}`);
    } catch (error) {
      setStatus('File upload failed.');
    }
  };

  return (
    <div className="container">
      <h1>Video Processing Pipeline</h1>
      <div className="upload-section">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>
      <div className="status">
        <h2>Status:</h2>
        <p>{status}</p>
      </div>
      {metadata && (
        <div className="metadata">
          <h2>Metadata:</h2>
          <pre>{JSON.stringify(metadata, null, 2)}</pre>
        </div>
      )}
      {enhancedVideoUrl && (
        <div className="video">
          <h2>Enhanced Video:</h2>
          <video controls src={enhancedVideoUrl} width="500" />
        </div>
      )}
    </div>
  );
}

export default App;