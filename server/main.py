from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from agents import safety_agent, main_agent, cleanup_agent
from agents.main_agent import clear_history
from tts import text_to_speech, get_wav_duration, generate_mouth_cues, clean_text

app = FastAPI()

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═════════════════════════════════════════════════════════════
#  PIPELINE
#  Safety → Main → Cleanup → TTS → MouthCues
# ═════════════════════════════════════════════════════════════
def run_pipeline(question: str, voice: str = "male"):
    """
    Runs the full 3-agent pipeline and returns
    (answer_text, audio_filename, mouth_cues).
    """

    # ── Agent 1: Safety ──────────────────────────────────────
    try:
        is_safe = safety_agent(question)
    except RuntimeError as e:
        return str(e), None, None

    if not is_safe:
        blocked_msg = "I'm sorry, I can't help with that. Please ask me something else."
        audio_file  = text_to_speech(blocked_msg, voice)
        duration    = get_wav_duration(audio_file)
        cues        = generate_mouth_cues(blocked_msg, duration)
        return blocked_msg, audio_file, cues

    # ── Agent 2: Main response ────────────────────────────────
    try:
        raw_response = main_agent(question)
    except RuntimeError as e:
        return str(e), None, None

    # ── Agent 3: Cleanup ──────────────────────────────────────
    try:
        cleaned = cleanup_agent(raw_response)
    except RuntimeError:
        cleaned = clean_text(raw_response)   # fallback to regex

    final_text = clean_text(cleaned)

    # ── TTS ───────────────────────────────────────────────────
    try:
        audio_file = text_to_speech(final_text, voice)
    except RuntimeError as e:
        print(f"[TTS Error] {e}")
        return final_text, None, None

    # ── Mouth cues ────────────────────────────────────────────
    duration   = get_wav_duration(audio_file)
    mouth_cues = generate_mouth_cues(final_text, duration)

    return final_text, audio_file, mouth_cues


# ═════════════════════════════════════════════════════════════
#  ROUTES
# ═════════════════════════════════════════════════════════════
class VoiceRequest(BaseModel):
    message: str
    voice:   str = "male"   # "male" | "female" | "indian"


@app.post("/voice-chat")
async def voice_chat(request: VoiceRequest):
    answer, audio_file, mouth_cues = run_pipeline(request.message, request.voice)

    if not answer:
        answer = "I'm sorry, I couldn't find an answer to your question."

    return {
        "audio_url":  f"http://localhost:8000/audio/{audio_file}" if audio_file else None,
        "mouthCues":  mouth_cues,
        "confidence": None,
    }


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = f"./{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    raise HTTPException(status_code=404, detail="File not found.")


@app.post("/clear-history")
async def clear_chat_history():
    """Clears the conversation memory — useful for starting a new session."""
    clear_history()
    return {"status": "Chat history cleared."}