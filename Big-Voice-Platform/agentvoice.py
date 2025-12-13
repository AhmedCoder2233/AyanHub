from fastapi import FastAPI, WebSocket
from gtts import gTTS
import io

app = FastAPI()

def text_to_speech(text:str):
    voice = gTTS(text=text, lang="en")
    convertToByte = io.BytesIO()
    voice.write_to_fp(convertToByte)
    convertToByte.seek(0)
    return convertToByte.read()

@app.websocket("/ws")
async def liveVoicing(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            reciving = await websocket.receive_text()
            print(f"User Text: {reciving}")
            texttosend = f"You said: {reciving}"
            byting = text_to_speech(text=texttosend)
            await websocket.send_bytes(byting)
    except Exception as e:
        print(f"An Exception Raised: {e}")

