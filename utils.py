# utils.py
from datetime import datetime

def build_itinerary_prompt(destination, dates, budget, interests, user_prefs=None):
    prompt = (
        f"Create a concise day-by-day itinerary for {destination} from {dates.get('start')} "
        f"to {dates.get('end')}. Budget: {budget}. Interests: {', '.join(interests)}. "
    )
    if user_prefs:
        prompt += f"User preferences: {user_prefs}. "
    prompt += "Keep it short and numbered by day with 2-4 activities per day."
    return prompt

def adapt_for_mood(itinerary_text, mood):
    """
    Use simple rule-based adjustment for quick prototype.
    For a production build, call the LLM to re-generate a variation.
    """
    if mood == "tired":
        # shorten each day to max 2 activities
        lines = itinerary_text.splitlines()
        new_lines = []
        for line in lines:
            if len(line.strip())==0:
                continue
            # naive: keep shorter string
            new_lines.append(line.split(".")[0] + " (shortened)")
        return "\n".join(new_lines)
    elif mood == "energetic":
        return itinerary_text + "\nAdd evening activities: local music or nightlife."
    elif mood == "rainy":
        return itinerary_text + "\nReplace outdoor activities with museums and indoor cafes."
    else:
        return itinerary_text
