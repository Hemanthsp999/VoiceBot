LilBot: voice bot

# Tech Stack

    1. Frontend: Streamlit
    2. Backend: Python
    3. LLM model: Gemini-2.0-flash
    4. AI Frameworks: LangChain
    5. STT (speech-to-text) model: Openai-whisper
    6. TTS (text-to-speech) model: gTTS(Google text-to-speech)

# API keys:

    Get api key from Google AI studio.
    Paste it in ".env" file at root of directory

    .env file:
    API_KEY = "your_api_key_here"

# How to install and run the project ?

1. Clone the Project

```bash
git clone "project_repo_url"
```

2. Enter Project dir

```bash
cd "project_dir"
```

3. create Environment

```bash
python3 -m venv env
```

4. Activate Enviornment

```bash
source env/bin/activate
```

5. Install dependencies using requirements.txt

```bash
pip install -r requirements.txt
```

6. Run the model

```bash
streamlit run app.py
```

# Demo video: 
![Demo Video](demo/demo_video.webm)
