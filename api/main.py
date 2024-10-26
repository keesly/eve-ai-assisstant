from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env.const import fixed_responses, mongo_uri
import uuid
from models.message import MessageRequest
from models.session import SessionRequest
from datetime import datetime as dt, timedelta
import openai
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
from google.cloud import speech
import os

# Set path to the service account JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "env/google_config.json"

app = FastAPI()
client = MongoClient(mongo_uri, server_api=ServerApi("1"))
db = client["EveAI"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for sessions (for simplicity)
sessions = {}

# Load Hugging Face model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


# Function to interact with ChatGPT
def ask_chatgpt(question):
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=question, max_tokens=150, temperature=0.7
    )
    return response.choices[0].text.strip()


# Function to perform a Google search
def google_search(query):
    # Implement Google search logic (you may use third-party APIs or web scraping)
    return f"Google search results for '{query}' are not implemented yet."


# Function to generate a response using DialoGPT
def generate_response(user_message, context):
    # Encode the input with the context
    input_ids = tokenizer.encode(
        user_message + tokenizer.eos_token, return_tensors="pt"
    )

    # Generate response from the model
    chat_history_ids = model.generate(
        input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )

    # Decode the response
    response = tokenizer.decode(
        chat_history_ids[:, input_ids.shape[-1] :][0], skip_special_tokens=True
    )

    return response


@app.post("/session_token")
async def session_token(request: SessionRequest):
    try:
        email = request.email
        session_id = ""
        now = dt.now()

        def create_session():
            id = str(uuid.uuid4())
            now = dt.now()
            db.sessions.insert_one(
                {
                    "email": email,
                    "uuid": id,
                    "google_API_calls": 0,
                    "chat_GPT_calls": 0,
                    "created_at": now,
                    "expires_at": now + timedelta(days=30),
                }
            )
            return id

        existing_session = db.sessions.find_one({"email": email})
        if existing_session:
            if existing_session["expires_at"] > now:
                session_id = str(existing_session["uuid"])
                return str(session_id)
            else:
                id = create_session()
        else:
            id = create_session()
        return id
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.post("/process_message")
async def process_message(request: MessageRequest):
    try:
        user_message = request.message.lower()
        session_id = request.session_id

        if session_id not in sessions:
            sessions[session_id] = {"history": []}

        context = sessions[session_id]
        context["history"].append({"user": user_message})

        # Check for fixed responses
        if user_message in fixed_responses:
            response = fixed_responses[user_message]
        # Check for keywords
        elif "analyze" in user_message or "describe" in user_message:
            chatgpt_response = ask_chatgpt(user_message)
            return {"message": chatgpt_response}

        elif "google" in user_message:
            search_query = user_message.replace("google", "").strip()
            google_response = google_search(search_query)
            return {"message": google_response}

        else:
            # Generate response using DialoGPT
            response = generate_response(user_message, context)

        context["history"].append({"eve": response})

        return {"message": response, "history": context["history"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    client = speech.SpeechClient()

    content = await audio.read()

    audio_data = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio_data)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return {"transcript": transcript}