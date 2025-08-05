import streamlit as st
from dotenv import load_dotenv
import os
from streamlit_mic_recorder import mic_recorder
from voice_bot import VoiceBot
import time

load_dotenv()

api = os.getenv("API_KEY")

voice_bot = VoiceBot()

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Centered Title
st.markdown("<h1 style='text-align: center;'>Voice Bot </h1>", unsafe_allow_html=True)

# Sidebar - History
with st.sidebar:
    st.markdown("### History")
    for i, (user, bot) in enumerate(st.session_state.history):
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Bot:** {bot}")
        st.markdown("---")


input = mic_recorder(start_prompt="Click to talk", stop_prompt="Stop recording", key="recorder")

if input:
    # Assume we're simulating a response for now
    user_input = "voice input"
    start = time.perf_counter()
    bot_response = voice_bot.bot(input)
    end = time.perf_counter()
    print(f"Response time: {end - start}")

    # Save to history
    st.session_state.history.append((user_input, bot_response))

    # Display
    st.markdown("### ou")
    st.audio(input["bytes"], format="audio/wav")

    st.markdown("### Bot")
    st.write(bot_response)
else:
    st.markdown("Click the mic icon above to speak!")


