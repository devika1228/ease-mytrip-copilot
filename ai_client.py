# ai_client.py
import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv(OPENAI_API_KEY, "")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

def call_llm(prompt, max_tokens=400, temperature=0.7):
    """
    Call OpenAI's completion endpoint (ChatCompletion or text completions).
    If OPENAI_API_KEY not set, return a mock response for demo.
    """
    if not OPENAI_KEY:
        # Mocked sample (keeps it deterministic and fast for offline demos)
        return ("Day 1: Morning - City walking tour. Lunch at local cafe. "
                "Afternoon - Museum visit. Evening - Leisure stroll.\n"
                "Day 2: Morning - Local market. Afternoon - River cruise.")
    try:
        # Use ChatCompletion (gpt-4o or gpt-4/3.5 depending on your access)
        # This example uses gpt-3.5-turbo style call
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"You are a helpful travel planner."},
                      {"role":"user","content":prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        text = resp["choices"][0]["message"]["content"].strip()
        return text
    except Exception as e:
        # Fallback
        return ("Day 1: Morning - Museum, Afternoon - Park, Evening - Local dinner.\n"
                "Day 2: Morning - City tour, Afternoon - Relaxation.")
