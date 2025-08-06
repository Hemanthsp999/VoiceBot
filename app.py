import pyttsx3
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice_bot import VoiceBot
import time

voice_bot = VoiceBot()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.markdown("<h1 style='text-align: center;'>Voice Bot </h1>", unsafe_allow_html=True)

# Sidebar - Chat history
with st.sidebar:
    st.markdown("### History")
    for user, bot in st.session_state.history:
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Bot:** {bot}")
        st.markdown("---")

# Record input from mic
input = mic_recorder(start_prompt="Click to talk", stop_prompt="Stop recording", key="recorder")

if input:
    user_input = "User spoke something"
    start = time.perf_counter()

    # Get bot text response
    bot_response = voice_bot.inputVoice(input)
    response = pyttsx3.speak(bot_response)
    print(f"Debug: {response}")
    end = time.perf_counter()

    # Save to chat history
    st.session_state.history.append((user_input, bot_response))

    # Display sections
    st.markdown("### Your Audio")
    st.audio(input["bytes"], format="audio/wav")

    st.markdown("### Bot Response (Text)")
    st.write(bot_response)

    st.markdown("### Bot Response (Audio)")

    st.markdown(f"🕒 **Response Time:** {end - start:.2f}s")
else:
    st.markdown("Click the mic icon above to speak!")

