import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pyttsx3
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

import os
import google.generativeai as genai

apiKey="AIzaSyApvWH5jct2jiyWwua2dqcSwHY5oJ9yn2c"
genai.configure(api_key=apiKey)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 50,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(history=[])





app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the definitions from the JSON file
# def load_definitions():
#     try:
#         with open("D:/Bala/Avatar chatbot/Avatar project/public/definitions.json", "r") as file:
#             data = json.load(file)
#         return data["definitions"]
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Definitions file not found.")



def clean_response(text):
    text = text.strip()
    text = text.replace("\n", " ")  # Replace newlines with spaces
    text = re.sub(r"\*\*", "", text)  # Remove **bold text**
    text = re.sub(r"\*", "", text)  # Remove * bullet points
    text = re.sub(r"_", "", text)  # Remove underscores (if any)
    return text

# Function to find an answer from the JSON file and get lipsync data
def get_response_and_lipsync(question):
    # definitions = load_definitions()
    # for entry in definitions:
    #     if question.lower() in entry["question"].lower():
    #         # Return answer and mouthCues data
    #         return entry["answer"], entry.get("mouthCues", [])
    # return None, None
    print(question)  # Debugging

    try:
        response = chat_session.send_message(question)
        cleaned_response = clean_response(response.text)
        print("Cleaned Response from API:", cleaned_response)  # Debugging
        return cleaned_response, None
    except Exception as e:
        print(f"Error in API call: {e}")
        return "I'm sorry, something went wrong.", None




# Text-to-speech conversion using pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()

    # Set properties for the speech engine
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    # Select voice for Indian English
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Indian" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    # Save speech to an audio file
    audio_file = "response.ogg"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()

    return audio_file

# Request model for user input
class VoiceRequest(BaseModel):
    message: str

# POST endpoint to handle voice interactions
@app.post("/voice-chat")
async def voice_chat(request: VoiceRequest):
    user_message = request.message

    # Find answer and mouthCues data in the JSON file
    answer, mouthCues = get_response_and_lipsync(user_message)
    
    # If no answer is found, provide a fallback response
    if answer is None:
        answer = "I'm sorry, I couldn't find an answer to your question."

    # Convert the answer to speech
    audio_file = text_to_speech(answer)

    # Return the audio file URL and mouthCues data
    return {
        "audio_url": f"http://localhost:8000/audio/{audio_file}",
        "mouthCues": mouthCues,
        "confidence": None,  # You can add confidence score logic here if needed
    }

# GET endpoint to retrieve the audio file
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = f"./{filename}"

    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/ogg")  # Changed to audio/ogg to match the saved format
    else:
        raise HTTPException(status_code=404, detail="File not found.")