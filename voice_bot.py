# from langchain_google_genai import ChatGoogleGenerativeAI
import io
import librosa
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage
import whisper

# doesn't require any rag. just a voice bot
prompt_template = """
                You are a helpful AI Assitant. Your task is to give answers for the {voiceInput}.
                Think throughly before giving any answers.
                ***Important Note***: Don't get halucinate or give any halucinate answers
"""


class VoiceBot:
    def __init__(self):

        self.whisper_model = whisper.load_model("tiny")
        self.llm_model = OllamaLLM(
            model="tinyllama:1.1b",
        )

        self.prompt = PromptTemplate.from_template(
            template=prompt_template
        )

    def processVoice(self, input):
        audio_stream = io.BytesIO(input["bytes"])
        audio_np, sr = librosa.load(audio_stream, sr=16000)
        print(f"Debug sample rate: {sr}")
        result = self.whisper_model.transcribe(audio_np)
        print(f"Debug Transcribe text: {result['text']}")
        return result["text"]

    def bot(self, voiceInput):
        userInput = self.processVoice(voiceInput)
        # make chain of prompt to llm
        chain = self.prompt | self.llm_model

        response = chain.invoke(userInput)
        return str(response)
