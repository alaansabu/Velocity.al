import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI , WebSocket ,Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv
load_dotenv()
OPEN_API_KEY = os.getenv('OPEN_AI_KEY')
PORT =  os.get('PORT',5000)

