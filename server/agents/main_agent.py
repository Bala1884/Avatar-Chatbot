import os
from groq import Groq

MAIN_MODEL = "llama-3.3-70b-versatile"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Full conversation history — persists across requests
chat_history = [
    {
        "role": "system",
        "content": (
            "You are ARIA, a helpful and friendly general-purpose AI assistant. "
            "Answer any topic clearly and conversationally. "
            "Never use markdown, bullet points, numbered lists, or special formatting. "
            "Respond in plain text only. Always complete your sentences fully."
            "Respond within 100 words and always complete the sentences."
        )
    }
]


def main_agent(user_message: str) -> str:
    """
    Agent 2 — Main Response (llama-3.3-70b-versatile via Groq)
    Generates a full response using the complete conversation history.
    """
    print(f"[Main Agent] User: {user_message}")

    chat_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model=MAIN_MODEL,
            messages=chat_history,
            max_tokens=300,
            temperature=0.8,
        )
        reply = response.choices[0].message.content.strip()

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        print(f"[Main Agent] Raw reply: {reply}")
        return reply

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