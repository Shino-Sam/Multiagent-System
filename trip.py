import os
from dotenv import load_dotenv
import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# --- Load GitHub Token securely ---
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# --- Setup DeepSeek client ---
endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# --- DeepSeek AI interaction function ---   
def ask_deepseek(prompt: str) -> str:
    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a very helpful, creative trip planner AI."),
                UserMessage(prompt),
            ],
            temperature=0.8,
            top_p=0.1,
            max_tokens=1024,
            model=model,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# --- Streamlit App Starts ---
st.set_page_config(page_title="🌎 AI Trip Planner", layout="wide")

st.title("🌟Trip Planner")
st.write("Plan your dream trip with multi-agent collaboration! ✈️🏨🎟️")

# --- Sidebar Inputs ---
st.sidebar.header("🛫 Trip Details")
destination = st.sidebar.text_input("Destination", placeholder="e.g., Paris, Tokyo")
days = st.sidebar.number_input("Number of Days", min_value=1, max_value=60, value=5)
travelers = st.sidebar.number_input("Number of Travelers", min_value=1, max_value=20, value=1)
interests = st.sidebar.text_input("Interests", placeholder="e.g., museums, food, hiking")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Options")
include_hotels = st.sidebar.checkbox("Include Hotels", value=True)
include_flights = st.sidebar.checkbox("Include Flight Suggestions", value=True)
include_weather = st.sidebar.checkbox("Include Weather Forecast", value=True)
include_events = st.sidebar.checkbox("Include Local Events", value=True)
include_security = st.sidebar.checkbox("Security and Fraud Checks", value=True)

# --- Plan Trip Button ---
if st.sidebar.button("✨ Plan My Trip"):
    with st.spinner("Planning your amazing trip..."):
        trip_prompt = f"""
        Plan a secure, exciting {days}-day trip to {destination} for {travelers} people.
        Focus on these interests: {interests}.
        Include detailed daily itineraries, activities, and safety recommendations.
        """
        trip_plan = ask_deepseek(trip_prompt)
        st.subheader("📋 Your Trip Plan:")
        st.write(trip_plan)

        # Store trip for download
        st.session_state.trip_plan = trip_plan

# --- Other Buttons ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏨 Get Hotel Recommendations"):
        with st.spinner("Finding best hotels..."):
            hotel_prompt = f"Suggest top hotels in {destination} for {travelers} people, considering safety and affordability."
            hotel_suggestions = ask_deepseek(hotel_prompt)
            st.subheader("🏨 Hotel Recommendations:")
            st.write(hotel_suggestions)

with col2:
    if st.button("✈️ Find Flight Options"):
        with st.spinner("Searching flights..."):
            flight_prompt = f"Find best flight options to {destination} for {travelers} people."
            flight_suggestions = ask_deepseek(flight_prompt)
            st.subheader("✈️ Flight Booking Suggestions:")
            st.write(flight_suggestions)

with col3:
    if st.button("☁️ Weather Forecast"):
        with st.spinner("Checking weather..."):
            weather_prompt = f"Give me the 5-day weather forecast for {destination}."
            weather_report = ask_deepseek(weather_prompt)
            st.subheader("☁️ Weather Forecast:")
            st.write(weather_report)

with col4:
    if st.button("🎭 Find Local Events"):
        with st.spinner("Finding cool events..."):
            events_prompt = f"List popular events happening in {destination} during the next {days} days."
            events_info = ask_deepseek(events_prompt)
            st.subheader("🎭 Local Event Finder:")
            st.write(events_info)

with col5:
    if st.button("🛡️ Security and Fraud Check"):
        with st.spinner("Checking security tips..."):
            security_prompt = f"Give me travel safety tips and common frauds to avoid in {destination}."
            security_info = ask_deepseek(security_prompt)
            st.subheader("🛡️ Security Tips and Fraud Protection:")
            st.write(security_info)

# --- Download Trip Plan Button ---
if "trip_plan" in st.session_state:
    st.download_button(
        label="📄 Download Trip Plan",
        data=st.session_state.trip_plan,
        file_name=f"{destination}_trip_plan.txt",
        mime="text/plain",
    )

# --- Live Trip Planning Chatbot ---
st.markdown("---")
st.header("💬 Trip Planning Chatbot")
st.write("Ask any custom questions about your trip!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Type your question here...")

if st.button("Ask"):
    if user_query:
        with st.spinner("AI is replying..."):
            bot_reply = ask_deepseek(f"You are an expert travel assistant. User asks: {user_query}")
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("AI", bot_reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")
