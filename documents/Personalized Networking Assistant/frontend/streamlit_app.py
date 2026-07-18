import streamlit as st
import requests
import json
from pathlib import Path
import sys

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services import feedback_logger

# Backend API URL
BASE_URL = "http://127.0.0.1:8000"
import streamlit as st
import requests
import sys
from pathlib import Path

# Allow importing backend modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services import feedback_logger

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 Personalized Networking Assistant")
st.markdown(
    "Generate AI-powered conversation starters for professional networking events."
)

# -------------------------
# Session State
# -------------------------
if "topics" not in st.session_state:
    st.session_state["topics"] = []

if "suggestions" not in st.session_state:
    st.session_state["suggestions"] = []

# ==========================
# Generate Conversation
# ==========================

st.header("Generate Conversation Starters")

event_description = st.text_area(
    "📝 Event Description",
    placeholder="Example: AI conference discussing Generative AI, LLMs and Robotics..."
)

user_interests = st.text_input(
    "🎯 Your Interests (comma-separated)",
    placeholder="Python, Machine Learning, Startups"
)

if st.button("Generate Conversation Starters"):

    if event_description and user_interests:

        payload = {
            "description": event_description,
            "interests": [
                interest.strip()
                for interest in user_interests.split(",")
            ]
        }

        try:
            response = requests.post(
                f"{BASE_URL}/generate-conversation",
                json=payload
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state["topics"] = data["topics"]
                st.session_state["suggestions"] = data["suggestions"]

                st.success("Conversation starters generated successfully!")

            else:
                st.error("Backend returned an error.")

        except Exception as e:
            st.error(f"Cannot connect to backend.\n\n{e}")

    else:
        st.warning("Please enter both event description and interests.")
# --- FEEDBACK HISTORY ---

st.markdown("---")
st.subheader("🗂 View Feedback History")

if st.button("Show Feedback", key="show_feedback"):
    feedback_path = Path("feedback.json")

    if feedback_path.exists():
        with open(feedback_path, "r") as f:
            feedback = json.load(f)

        if feedback:
            for item in reversed(feedback[-10:]):  # Show latest 10
                st.markdown(f"**🕒 {item['timestamp']}**")
                st.write("**Suggestion:**", item["suggestion"])
                st.write("**Feedback:**", item["feedback"])
                st.markdown("---")
        else:
            st.info("No feedback recorded yet.")
    else:
        st.info("No feedback file found.")

# ==========================
# Display Results
# ==========================

if st.session_state["topics"]:

    st.divider()

    st.header("Extracted Event Themes")

    for topic in st.session_state["topics"]:
        st.success(topic)

    st.header("Conversation Starters")

    for suggestion in st.session_state["suggestions"]:

        col1, col2, col3 = st.columns([8,1,1])

        with col1:
            st.write("• " + suggestion)

        with col2:
            if st.button("👍", key=f"like_{suggestion}"):

                feedback_logger.log_feedback(
                    suggestion,
                    "like"
                )

                st.success("Feedback saved.")

        with col3:
            if st.button("👎", key=f"dislike_{suggestion}"):

                feedback_logger.log_feedback(
                    suggestion,
                    "dislike"
                )

                st.success("Feedback saved.")

# ==========================
# Fact Checker
# ==========================

st.divider()

st.header("Wikipedia Fact Checker")

query = st.text_input(
    "Enter a topic",
    placeholder="Artificial Intelligence"
)

if st.button("Fact Check"):

    if query:

        response = requests.post(
            f"{BASE_URL}/fact-check",
            json={
                "query": query
            }
        )

        if response.status_code == 200:

            st.info(response.json()["summary"])

        else:

            st.error("Fact check failed.")

# ==========================
# Conversation History
# ==========================

st.divider()

st.header("Conversation History")

if st.button("Load History"):

    try:

        response = requests.get(
            f"{BASE_URL}/history"
        )

        if response.status_code == 200:

            history = response.json()

            if history:

                for item in history[::-1]:

                    with st.expander(item["timestamp"]):

                        st.write("**Description:**")
                        st.write(item["description"])

                        st.write("**Interests:**")
                        st.write(", ".join(item["interests"]))

                        st.write("**Topics:**")
                        st.write(", ".join(item["topics"]))

                        st.write("**Suggestions:**")

                        for s in item["suggestions"]:
                            st.write("- " + s)

            else:

                st.info("No conversation history available.")

        else:

            st.error("Unable to load history.")

    except Exception as e:
        st.error(f"Unable to load history: {e}")

# ==========================
# Feedback History
# ==========================

st.divider()

st.header("Feedback History")

if st.button("Show Feedback"):

    feedback = feedback_logger.get_feedback()

    if feedback:

        for item in feedback[::-1]:

            st.write("---")

            st.write("Suggestion:")
            st.write(item["suggestion"])

            st.write("Feedback:")
            st.write(item["feedback"])

            st.write("Time:")
            st.write(item["timestamp"])

    else:

        st.info("No feedback available.")
# --- DISPLAY RESULTS + FEEDBACK ---

if "suggestions" in st.session_state:

    st.subheader("🧠 Extracted Topics:")
    st.write(st.session_state["topics"])

    st.subheader("💬 Conversation Starters:")

    for i, suggestion in enumerate(st.session_state["suggestions"]):

        st.markdown(f"- {suggestion}")

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("👍", key=f"like_{i}"):

                feedback_logger.log_feedback(
                    suggestion,
                    "like"
                )

                st.success("Thanks for the feedback!")

        with col2:
            if st.button("👎", key=f"dislike_{i}"):

                feedback_logger.log_feedback(
                    suggestion,
                    "dislike"
                )

                st.info("Feedback noted.")
# --- FACT CHECK SECTION ---

st.markdown("---")
st.subheader("🔍 Quick Fact-Check")

query = st.text_input("Enter a topic to fact-check")

if st.button("Fact Check", key="fact_check_button"):
    if query:
        response = requests.post(
            f"{BASE_URL}/fact-check",
            json={"query": query}
        )

        if response.status_code == 200:
            st.success(response.json()["summary"])
        else:
            st.error("Fact-checking failed.")
    else:
        st.warning("Please enter a topic.")