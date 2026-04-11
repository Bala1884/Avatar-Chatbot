import os
from groq import Groq

CLEANUP_MODEL = "llama-3.3-70b-versatile"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def cleanup_agent(raw_response: str) -> str:
    """
    Agent 3 — Cleanup (llama-3.3-70b-versatile via Groq)
    Removes markdown, ensures complete sentences, plain text only.
    """
    print("[Cleanup Agent] Cleaning response...")

    try:
        response = client.chat.completions.create(
            model=CLEANUP_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a text cleanup assistant for a text-to-speech avatar. "
                        "Take the given response and clean it up following these rules strictly: "
                        "1. Remove all markdown — no **, *, #, bullet points, numbered lists, or underscores. "
                        "2. Ensure the response ends on a complete sentence — never cut off mid-sentence. "
                        "3. Keep the full meaning — do not summarize or remove important content. "
                        "4. Output plain text only. No explanations or meta-commentary. "
                        "5. Do not add anything new — only clean what is already there. "
                        "Return only the cleaned response text, nothing else."
                    )
                },
                {"role": "user", "content": raw_response}
            ],
            max_tokens=400,
            temperature=0.1,
        )
        cleaned = response.choices[0].message.content.strip()
        print(f"[Cleanup Agent] Cleaned: {cleaned}")
        return cleaned

    except Exception as e:
        print(f"[Cleanup Agent] Error: {e}")
        return raw_response  # fallback to raw if cleanup fails