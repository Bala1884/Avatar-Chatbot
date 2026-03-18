import os
import re
import wave
import subprocess

# ── PIPER CONFIG ──────────────────────────────────────────────
PIPER_EXE = "./piper/piper.exe"

VOICES = {
    "male":   "./piper/en_US-ryan-medium.onnx",
    "female": "./piper/en_US-kathleen-low.onnx",
    "indian": "./piper/en_US-kusal-medium.onnx",
}
DEFAULT_VOICE = "male"


# ═════════════════════════════════════════════════════════════
#  PIPER TTS
# ═════════════════════════════════════════════════════════════
def text_to_speech(text: str, voice_key: str = DEFAULT_VOICE) -> str:
    """
    Runs Piper TTS to generate a WAV file.
    Returns the filename of the generated audio.
    """
    voice_model = VOICES.get(voice_key, VOICES[DEFAULT_VOICE])
    audio_file  = "response.wav"

    if not os.path.exists(PIPER_EXE):
        raise RuntimeError(
            f"Piper not found at {PIPER_EXE}. "
            "Download from https://github.com/rhasspy/piper/releases "
            "and place piper.exe + voice models in ./piper/"
        )

    if not os.path.exists(voice_model):
        raise RuntimeError(
            f"Voice model not found: {voice_model}. "
            "Download from https://huggingface.co/rhasspy/piper-voices"
        )

    try:
        result = subprocess.run(
            [PIPER_EXE, "--model", voice_model, "--output_file", audio_file],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Piper error: {result.stderr.decode()}")
        print(f"[TTS] Generated {audio_file} with voice: {voice_key}")
        return audio_file

    except subprocess.TimeoutExpired:
        raise RuntimeError("Piper TTS timed out.")


# ═════════════════════════════════════════════════════════════
#  WAV DURATION
# ═════════════════════════════════════════════════════════════
def get_wav_duration(filepath: str) -> float:
    """Returns duration of a WAV file in seconds."""
    try:
        with wave.open(filepath, "r") as wf:
            return wf.getnframes() / float(wf.getframerate())
    except Exception:
        return 3.0  # fallback


# ═════════════════════════════════════════════════════════════
#  MOUTH CUES GENERATION
#
#  Viseme letter map matches your frontend `corresponding` obj:
#  A→viseme_PP, B→viseme_kk, C→viseme_I,  D→viseme_AA,
#  E→viseme_O,  F→viseme_U,  G→viseme_FF, H→viseme_TH, X→viseme_PP
# ═════════════════════════════════════════════════════════════

PHONEME_TO_VISEME = {
    "p": "A", "b": "A", "m": "A",           # Bilabials
    "f": "G", "v": "G",                      # Labiodentals
    "th": "H",                               # Dentals
    "t": "B", "d": "B", "n": "B",           # Alveolars
    "k": "B", "g": "B", "ng": "B",          # Velars
    "sh": "B", "ch": "B", "zh": "B",        # Postalveolar
    "s": "B", "z": "B",                     # Sibilants
    "l": "B", "r": "D",                     # Sonorants
    "w": "F", "y": "C",                     # Glides
    "a": "D", "ah": "D", "aw": "D",        # Open vowels
    "e": "C", "eh": "C", "ey": "C",        # Front vowels
    "i": "C", "ih": "C", "iy": "C",        # High front vowels
    "o": "E", "oh": "E", "ow": "E",        # Mid-back vowels
    "u": "F", "uh": "F", "uw": "F",        # High back vowels
}


def word_to_visemes(word: str) -> list:
    """Convert a single word to a list of viseme letters."""
    word = word.lower().strip(".,!?;:'\"()-")
    visemes = []
    i = 0
    while i < len(word):
        digraph = word[i:i+2]
        if digraph in PHONEME_TO_VISEME:
            visemes.append(PHONEME_TO_VISEME[digraph])
            i += 2
        elif word[i] in PHONEME_TO_VISEME:
            visemes.append(PHONEME_TO_VISEME[word[i]])
            i += 1
        else:
            visemes.append("X")
            i += 1
    return visemes if visemes else ["X"]


def generate_mouth_cues(text: str, audio_duration: float) -> list:
    """
    Generate timed mouthCues from text + actual audio duration.
    Distributes visemes proportionally across the real audio length.
    """
    words = [w for w in text.split() if w.strip()]
    if not words:
        return [{"start": 0.0, "end": audio_duration, "value": "X"}]

    # Build weighted viseme list
    all_cues = []
    for word in words:
        for v in word_to_visemes(word):
            # Vowels get slightly more time than consonants
            weight = 1.5 if v in ("C", "D", "E", "F") else 1.0
            all_cues.append((v, weight))
        all_cues.append(("X", 0.4))   # short pause between words

    # Remove trailing silence
    while all_cues and all_cues[-1][0] == "X":
        all_cues.pop()

    if not all_cues:
        return [{"start": 0.0, "end": audio_duration, "value": "X"}]

    total_weight = sum(w for _, w in all_cues)
    mouth_cues   = []
    current_time = 0.0

    for viseme, weight in all_cues:
        duration = (weight / total_weight) * audio_duration
        mouth_cues.append({
            "start": round(current_time, 3),
            "end":   round(current_time + duration, 3),
            "value": viseme,
        })
        current_time += duration

    print(f"[MouthCues] {len(mouth_cues)} cues over {audio_duration:.2f}s")
    return mouth_cues


# ═════════════════════════════════════════════════════════════
#  REGEX CLEANER — strips leftover markdown
# ═════════════════════════════════════════════════════════════
def clean_text(text: str) -> str:
    text = text.strip()
    text = text.replace("\n", " ")
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*",   "", text)
    text = re.sub(r"_",    "", text)
    text = re.sub(r"#+\s", "", text)
    text = re.sub(r"\s+",  " ", text)
    return text.strip()