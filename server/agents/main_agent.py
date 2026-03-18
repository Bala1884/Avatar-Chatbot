import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MAIN_MODEL = "llama3.2:3b"

# Full conversation history — persists across requests
chat_history = [
    {
        "role": "system",
        "content": (
            "You are ARIA, a helpful and friendly general-purpose AI assistant. "
            "Answer any topic clearly and conversationally. "
            "Never use markdown, bullet points, numbered lists, or special formatting. "
            "Respond in plain text only. Always complete your sentences fully."
        )
    }
]


def main_agent(user_message: str) -> str:
    """
    Agent 2 — Main Response (llama3.2:3b)
    Generates a full response using the complete conversation history.
    """
    print(f"[Main Agent] User: {user_message}")

    # Add user message to persistent history
    chat_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MAIN_MODEL,
                "messages": chat_history,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "top_k": 40,
                    "num_predict": 300,
                },
            },
            timeout=120,
        )
        response.raise_for_status()
        reply = response.json()["message"]["content"].strip()

        # Save reply to history for memory
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        print(f"[Main Agent] Raw reply: {reply}")
        return reply

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Ollama is not running. Start it with: ollama serve")
    except Exception as e:
        raise RuntimeError(f"Main agent failed: {e}")


def clear_history():
    """Clears chat history but keeps the system prompt."""
    chat_history.clear()
    chat_history.append({
        "role": "system",
        "content": (
            "You are ARIA, a helpful and friendly general-purpose AI assistant. "
            "Answer any topic clearly and conversationally. "
            "Never use markdown, bullet points, numbered lists, or special formatting. "
            "Respond in plain text only. Always complete your sentences fully."
        )
    })
    print("[Main Agent] Chat history cleared.")