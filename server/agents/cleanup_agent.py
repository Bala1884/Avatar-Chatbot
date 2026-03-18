import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MAIN_MODEL = "llama3.2:3b"


def cleanup_agent(raw_response: str) -> str:
    """
    Agent 3 — Cleanup (llama3.2:3b)
    Removes markdown, ensures complete sentences, plain text only.
    """
    print("[Cleanup Agent] Cleaning response...")

    system = (
        "You are a text cleanup assistant for a text-to-speech avatar. "
        "Take the given response and clean it up following these rules strictly: "
        "1. Remove all markdown — no **, *, #, bullet points, numbered lists, or underscores. "
        "2. Ensure the response ends on a complete sentence — never cut off mid-sentence. "
        "3. Keep the full meaning — do not summarize or remove important content. "
        "4. Output plain text only. No explanations or meta-commentary. "
        "5. Do not add anything new — only clean what is already there. "
        "Return only the cleaned response text, nothing else."
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MAIN_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": raw_response},
                ],
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 400},
            },
            timeout=60,
        )
        response.raise_for_status()
        cleaned = response.json()["message"]["content"].strip()
        print(f"[Cleanup Agent] Cleaned: {cleaned}")
        return cleaned

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Ollama is not running. Start it with: ollama serve")
    except Exception as e:
        raise RuntimeError(f"Cleanup agent failed: {e}")