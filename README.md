# EaseMyTrip Copilot - Prototype (Hackathon)

**One-line:** AI-powered travel companion prototype demonstrating conversational itinerary generation, mood-aware replanning, and disruption simulation.

## What this prototype demonstrates
- Generate a day-by-day itinerary from user inputs using an LLM (OpenAI/Vertex).
- Mood-aware replanning: select `Tired` / `Energetic` / `Rainy` and see itinerary adjust.
- Simulate disruptions (mock weather/flight) that trigger auto replanning.

## Tech stack (prototype)
- Streamlit (UI + logic)
- OpenAI API (LLM) — replace with Vertex if available
- Simple in-memory storage for generated itineraries

## Quickstart (local)
1. Clone repo
2. `python -m venv venv && source venv/bin/activate` (Mac/Linux) or `python -m venv venv && venv\\Scripts\\activate` (Windows)
3. `pip install -r requirements.txt`
4. Create a `.env` file with:
