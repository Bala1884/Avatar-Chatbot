import requests

OLLAMA_URL  = "http://localhost:11434/api/chat"
AGENT_MODEL = "gemma2:2b"


def safety_agent(user_message: str) -> bool:
    """
    Agent 1 — Safety Check (gemma2:2b)
    Returns True if message is safe, False if it should be blocked.
    """
    print(f"[Safety Agent] Checking: {user_message}")

    system = (
        "You are a content safety classifier. "
        "Reply with exactly one word: SAFE or UNSAFE. "
        "Mark UNSAFE if the message asks for: violence, self-harm, illegal activities, "
        "explicit sexual content, hate speech, or personal private data of others. "
        "Mark SAFE for everything else including general questions, professional topics, "
        "casual conversation, opinions, facts, and any normal topic. "
        "Do not explain. Output only: SAFE or UNSAFE."
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": AGENT_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_message},
                ],
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 5},
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()["message"]["content"].strip()
        is_safe = "SAFE" in result.upper() and "UNSAFE" not in result.upper()
        print(f"[Safety Agent] Result: {result} → {'PASS' if is_safe else 'BLOCK'}")
        return is_safe

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Ollama is not running. Start it with: ollama serve")
    except Exception as e:
        raise RuntimeError(f"Safety agent failed: {e}")