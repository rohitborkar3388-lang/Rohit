"""
Flask Backend for Environmental Awareness Chatbot
Handles chat requests and returns AI-generated responses
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import json
import os
from datetime import datetime
import nltk
from nltk.stem import PorterStemmer
import re
import random
import openai

# ------------------------------------------------------------------
# NLTK SETUP (SAFE & CORRECT)
# ------------------------------------------------------------------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ------------------------------------------------------------------
# APP CONFIG
# ------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

stemmer = PorterStemmer()

model = None
intents_data = None

MODEL_NAME = os.getenv('MODEL_NAME', 'local')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# ------------------------------------------------------------------
# UTIL FUNCTIONS
# ------------------------------------------------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = nltk.word_tokenize(text)
    return ' '.join(stemmer.stem(word) for word in words)

def load_model():
    global model, intents_data

    if not os.path.exists('model.pkl'):
        return False, "Model not found. Please run train.py first."

    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)

        with open('intents_data.pkl', 'rb') as f:
            intents_data = pickle.load(f)

        return True, "Model loaded successfully"
    except Exception as e:
        return False, str(e)

# ------------------------------------------------------------------
# CHAT LOGIC
# ------------------------------------------------------------------
HUMAN_OPENERS = [
    "Got you.", "Good question.", "Alright—here’s the idea:",
    "Sure thing.", "Okay, so…"
]

FALLBACKS = [
    "I didn’t fully get that. Can you rephrase?",
    "Try asking with keywords like climate, recycling, or pollution."
]

def get_response(user_input):
    if MODEL_NAME.lower().startswith('gpt'):
        return get_response_openai(user_input)

    if model is None or intents_data is None:
        return {"text": "Model not loaded.", "tag": None, "confidence": 0.0}

    processed = preprocess_text(user_input)
    tag = model.predict([processed])[0]

    for intent in intents_data["intents"]:
        if intent["tag"] == tag:
            return {
                "text": f"{random.choice(HUMAN_OPENERS)} {random.choice(intent['responses'])}",
                "tag": tag,
                "confidence": 1.0
            }

    return {"text": random.choice(FALLBACKS), "tag": "fallback", "confidence": 0.0}

def get_response_openai(user_input):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an environmental awareness assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return {
        "text": response['choices'][0]['message']['content'],
        "tag": "provider",
        "confidence": 1.0
    }

# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '').strip()

    if not msg:
        return jsonify({'success': False, 'error': 'Empty message'}), 400

    result = get_response(msg)

    return jsonify({
        'success': True,
        'response': result['text'],
        'timestamp': datetime.now().strftime('%H:%M'),
        'tag': result.get('tag'),
        'confidence': result.get('confidence')
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None
    })

# ------------------------------------------------------------------
# START SERVER
# ------------------------------------------------------------------
if __name__ == '__main__':
    print("Starting Environmental Awareness Chatbot...")
    success, msg = load_model()
    print(msg)

    app.run(host='127.0.0.1', port=5000, debug=True)
