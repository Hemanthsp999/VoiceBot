import io
import base64
from gtts import gTTS
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice_bot import VoiceBot
import time
import streamlit.components.v1 as components

if "voice_bot" not in st.session_state:
    st.session_state.voice_bot = VoiceBot()

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.markdown("<h1 style='text-align: center;'>LilBot: AI voice bot</h1>", unsafe_allow_html=True)

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
    bot_response = st.session_state.voice_bot.inputVoice(input)
    # response = pyttsx3.speak(bot_response)
    response = gTTS(bot_response)
    mp3_f = io.BytesIO()
    response.write_to_fp(mp3_f)
    mp3_f.seek(0)

    mp_3_bytes = mp3_f.read()
    b64 = base64.b64encode(mp_3_bytes).decode()

    print(f"Debug: {response}")
    end = time.perf_counter()

    # Save to chat history
    st.session_state.history.append((user_input, bot_response))

    # User Audio if needed
    # st.markdown("### Your Audio")
    # st.audio(input["bytes"], format="audio/wav")

    st.markdown("### Bot Response")

    components.html(
        f"""
    <html>
    <body>
        <script>
            var audio = new Audio("data:audio/mp3;base64,{b64}");
            audio.play().catch(error => {{
                console.warn("Autoplay failed:", error);
                setTimeout(() => audio.play(), 500);
            }});
        </script>
    </body>
    </html>
    """,
        height=0,
    )
    st.write(bot_response)

    st.markdown(f"**Response Time:** {end - start:.2f}s")
else:
    st.markdown("Click the mic icon above to speak!")

