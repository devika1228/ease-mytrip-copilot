# app.py
import streamlit as st
from ai_client import call_llm
from mock_services import get_mock_weather, get_mock_flight_status
from utils import build_itinerary_prompt, adapt_for_mood
from PIL import Image
import json, os

st.set_page_config(page_title="EaseMyTrip Copilot - Prototype", layout="wide")

# Simple in-memory state for prototype
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
if "destination" not in st.session_state:
    st.session_state.destination = "Paris"

st.title("EaseMyTrip Copilot — Prototype")
st.markdown("AI-powered travel companion — demo prototype")

# Left column: Inputs
col1, col2 = st.columns([1,2])
with col1:
    st.header("Trip Input")
    destination = st.text_input("Destination", value=st.session_state.destination)
    st.session_state.destination = destination
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    budget = st.selectbox("Budget", ["Low", "Medium", "High"])
    interests = st.multiselect("Interests (choose up to 3)", ["museums","food","nature","architecture","shopping","nightlife"], default=["museums","food"])
    user_prefs = st.text_area("Other preferences (optional)", value="", max_chars=250)
    if st.button("Generate Itinerary"):
        # Build prompt and call LLM
        dates = {"start": start_date.strftime("%Y-%m-%d"), "end": end_date.strftime("%Y-%m-%d")}
        prompt = build_itinerary_prompt(destination, dates, budget, interests, user_prefs)
        with st.spinner("Generating itinerary via LLM..."):
            itinerary_text = call_llm(prompt)
        st.session_state.itinerary = itinerary_text

    st.markdown("---")
    st.header("Simulate Disruption")
    if st.button("Simulate Weather (Mock)"):
        w = get_mock_weather(destination)
        st.info(f"Mock weather for {destination}: {w['condition']}, {w['temp_c']}°C")
        # naive replan: if rainy, adapt
        if st.session_state.itinerary:
            new_it = adapt_for_mood(st.session_state.itinerary, "rainy")
            st.session_state.itinerary = new_it
    if st.button("Simulate Flight Status (Mock)"):
        f = get_mock_flight_status()
        st.info(f"Mock flight status: {json.dumps(f)}")
        if f.get("status") == "delayed" and st.session_state.itinerary:
            # simple change: append note to itinerary
            st.session_state.itinerary += f"\nNote: Flight delayed by {f.get('delay_minutes', 0)} minutes — adjust travel time."

with col2:
    st.header("Itinerary Preview")
    if st.session_state.itinerary:
        st.code(st.session_state.itinerary)
    else:
        st.info("Generate an itinerary to preview it here.")

    st.markdown("---")
    st.header("Mood Toggle")
    mood = st.radio("How are you feeling?", ["Neutral", "Tired", "Energetic", "Rainy"])
    if st.button("Apply Mood"):
        if not st.session_state.itinerary:
            st.warning("Generate an itinerary first.")
        else:
            if mood == "Neutral":
                st.session_state.itinerary = st.session_state.itinerary  # no change
            elif mood == "Tired":
                st.session_state.itinerary = adapt_for_mood(st.session_state.itinerary, "tired")
            elif mood == "Energetic":
                st.session_state.itinerary = adapt_for_mood(st.session_state.itinerary, "energetic")
            elif mood == "Rainy":
                st.session_state.itinerary = adapt_for_mood(st.session_state.itinerary, "rainy")
            st.success(f"Applied mood: {mood}")

    st.markdown("---")
    st.header("AI Postcard")
    if st.button("Generate Postcard"):
        if not st.session_state.itinerary:
            st.warning("Generate an itinerary first.")
        else:
            # Build small prompt to summarize day(s)
            sample_summary_prompt = ("Summarize the following itinerary into a warm 2-sentence travel postcard "
                                     "highlighting key experiences (friendly tone):\n\n" + st.session_state.itinerary)
            postcard_text = call_llm(sample_summary_prompt, max_tokens=120, temperature=0.8)
            st.success("AI Postcard generated:")
            st.write(postcard_text)
            # show sample image from assets
            img_path = os.path.join("assets", "sample_postcard.jpg")
            if os.path.exists(img_path):
                st.image(img_path, caption="Sample Postcard Image")

# Bottom: Quick demo notes
st.markdown("---")
st.markdown("**Demo Notes:** Use `Generate Itinerary`, then `Simulate Weather` or `Apply Mood` to show re-planning. Click `Generate Postcard` to show the generative memory.")
