import os
from groq import Groq

SAFETY_MODEL = "llama-3.1-8b-instant"   # fast, cheap, enough for SAFE/UNSAFE
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def safety_agent(user_message: str) -> bool:
    """
    Agent 1 — Safety Check (llama-3.1-8b-instant via Groq)
    Returns True if message is safe, False if it should be blocked.
    """
    print(f"[Safety Agent] Checking: {user_message}")

    try:
        response = client.chat.completions.create(
            model=SAFETY_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a content safety classifier. "
                        "Reply with exactly one word: SAFE or UNSAFE. "
                        "Mark UNSAFE if the message asks for: violence, self-harm, illegal activities, "
                        "explicit sexual content, hate speech, or personal private data of others. "
                        "Mark SAFE for everything else including general questions, professional topics, "
                        "casual conversation, opinions, facts, and any normal topic. "
                        "Do not explain. Output only: SAFE or UNSAFE."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=5,
            temperature=0.1,
        )
        result  = response.choices[0].message.content.strip()
        is_safe = "SAFE" in result.upper() and "UNSAFE" not in result.upper()
        print(f"[Safety Agent] Result: {result} → {'PASS' if is_safe else 'BLOCK'}")
        return is_safe

    except Exception as e:
        print(f"[Safety Agent] Error: {e}")
        return True  # fail open