import io
import os
from dotenv import load_dotenv
import librosa
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import whisper

load_dotenv()

api = os.getenv("API_KEY")

prompt = """
{history}

You are LilBot, a helpful AI voice assistant designed to provide accurate, conversational responses to spoken queries.

## Core Instructions:
- Respond to the user's voice input: "{input}"
- Provide concise, clear answers optimized for audio delivery
- Use natural, conversational language that sounds good when spoken aloud
- Keep responses between 1-3 sentences unless more detail is specifically requested

## Tone:
- Friendly and approachable
- Professional but conversational

"""


class VoiceBot:
    def __init__(self):
        # Load whisper model
        self.whisper_model = whisper.load_model("tiny")

        # LLM model from Gemini
        self.llm_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001",
            google_api_key=api,
            temperature="0.5",
            max_tokens=None,
            timeout=None,
            max_retries=5
        )

        self.prompt = PromptTemplate.from_template(
            template=prompt
        )

        self.memory = ConversationBufferMemory(memory_key="history", input_key="input")

        # Use ConversationChain to automatically handle 'history'
        self.chain = ConversationChain(
            llm=self.llm_model,
            prompt=self.prompt,
            memory=self.memory,
            input_key="input",
            verbose=True
        )

    def processVoice(self, input):
        # Read bytes from audio input
        audio_stream = io.BytesIO(input["bytes"])
        audio_np, sr = librosa.load(audio_stream, sr=16000)
        print(f"Debug sample rate: {sr}")
        result = self.whisper_model.transcribe(audio_np)
        print(f"Debug Transcribe text: {result['text']}")
        return result["text"]

    def inputVoice(self, voiceInput):
        userInput = self.processVoice(voiceInput)
        response = self.chain.invoke({"input": userInput})
        return response["response"]

