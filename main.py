
from fastapi import FastAPI , WebSocket ,Request
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import numpy as np
import asyncio
from typing import List
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    
    title="Real time audio processing",
    description="process transcribe audio in realtime"
    
)

app.add_middleware(
    CORSMiddleware,
    allow_orgins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_model = whisper.model('base')
    
class AudionProcessor:
    def  __init__(Self):
        self.buffer :list[bytes]
        self.processing : False
        
        
    async def process_audio(self,audio_chunks:bytes) -> str:
        self.buffer.append(audio_chunks)

        if len(self.buffer)>= 10 and not self.processing:
            self.processing:True
            
            try:
            
                audio_data = np.frombuffer(b''.join(self.buffer), dtype=np.float32)
                result = load_model.transcribe(audio_data)
                
                self.buffer = []
                return result['text']
            finally:
                self.processing = False
                return ''
audio_processor = AudionProcessor()


@app.websocket('ws/audio')
async def websocketEndpoint(wbskt:WebSocket):
    await wbskt.accept()
    while True:
        audio_chunk = await  WebSocket.receive_bytes()