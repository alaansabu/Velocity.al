
from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import whisper
import numpy as np
import asyncio
import tempfile
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Real-time Audio Processing",
    description="Process and transcribe audio in real-time using OpenAI Whisper"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Load Whisper model (options: tiny, base, small, medium, large)
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Model loaded successfully!")


class AudioProcessor:
    def __init__(self):
        self.buffer: List[bytes] = []
        self.processing: bool = False
        self.sample_rate: int = 16000  # Whisper expects 16kHz audio
        
    async def process_audio(self, audio_chunk: bytes) -> str:
        """Process audio chunks and return transcription when buffer is full."""
        self.buffer.append(audio_chunk)
        
        # Process when we have enough audio data (10 chunks) and not currently processing
        if len(self.buffer) >= 10 and not self.processing:
            self.processing = True
            
            try:
                # Combine all audio chunks
                audio_bytes = b''.join(self.buffer)
                
                # Convert bytes to numpy array (assuming float32 PCM audio)
                audio_data = np.frombuffer(audio_bytes, dtype=np.float32)
                
                # Ensure audio is the right shape for Whisper
                if len(audio_data) > 0:
                    # Transcribe the audio
                    result = model.transcribe(audio_data, fp16=False)
                    self.buffer = []
                    return result.get('text', '').strip()
                    
            except Exception as e:
                print(f"Transcription error: {e}")
            finally:
                self.processing = False
        
        return ''
    
    def clear_buffer(self):
        """Clear the audio buffer."""
        self.buffer = []
        self.processing = False


audio_processor = AudioProcessor()


@app.get("/")
async def root():
    """Serve the main HTML page."""
    html_path = static_path / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "running", "message": "Voice-to-Text API is active"}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe an uploaded audio file.
    Supports: mp3, wav, m4a, webm, and other formats supported by Whisper.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No audio file provided")
    
    # Create a temporary file to save the uploaded audio
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Transcribe the audio file
        result = model.transcribe(temp_path, fp16=False)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return JSONResponse(content={
            "success": True,
            "text": result.get("text", "").strip(),
            "language": result.get("language", "unknown"),
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                }
                for seg in result.get("segments", [])
            ]
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming and transcription.
    Send audio chunks as binary data and receive transcriptions as text.
    """
    await websocket.accept()
    print("WebSocket connection established")
    
    # Create a dedicated processor for this connection
    processor = AudioProcessor()
    
    try:
        while True:
            # Receive audio chunk from client
            audio_chunk = await websocket.receive_bytes()
            
            # Process the audio and get transcription
            transcription = await processor.process_audio(audio_chunk)
            
            # Send transcription back if we have one
            if transcription:
                await websocket.send_json({
                    "type": "transcription",
                    "text": transcription
                })
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        processor.clear_buffer()
        print("WebSocket connection closed")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("Voice-to-Text API started!")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("Voice-to-Text API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 