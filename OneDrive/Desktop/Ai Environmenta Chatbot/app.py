"""
Flask Backend for Environmental Awareness Chatbot
Handles chat requests and returns AI-generated responses
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import json
import os
import openai
from datetime import datetime
import nltk
from nltk.stem import PorterStemmer
import re
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        nltk.download('punkt', quiet=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize stemmer
stemmer = PorterStemmer()

# Global variables for model and intents
model = None
intents_data = None

# Model configuration: use LOCAL ('local') or a provider model name (e.g. 'gpt-5-mini')
MODEL_NAME = os.getenv('MODEL_NAME', 'local')
# OpenAI API key (for provider-based models)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def preprocess_text(text):
    """
    Preprocess text: convert to lowercase, remove special characters,
    and apply stemming
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = nltk.word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed_words)

def load_model():
    """
    Load the trained model and intents data
    """
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
        return False, f"Error loading model: {str(e)}"

HUMAN_OPENERS = [
    "Got you.",
    "Yep — here’s the gist.",
    "Good question.",
    "Alright, quick breakdown:",
    "Okay, so…",
    "Sure thing.",
    "Love that you’re asking this."
]

FOLLOW_UPS = {
    "climate_change": [
        "Want the main causes, the effects, or what you can do personally?",
        "Do you want a super short summary or the detailed version?"
    ],
    "pollution": [
        "Are you more worried about air, water, or plastic pollution?",
        "Want a few easy ways to reduce pollution day-to-day?"
    ],
    "recycling": [
        "Tell me what item you’re trying to recycle and I’ll help you sort it.",
        "Want a quick checklist for recycling correctly?"
    ],
    "plastic_waste": [
        "Want easy swaps to cut single‑use plastic?",
        "Are you dealing with plastic at home, school, or work?"
    ],
    "water_conservation": [
        "Do you want tips for home, gardening, or both?",
        "Want the top 5 easiest water-saving moves?"
    ],
    "sustainable_living": [
        "What’s your goal: save money, reduce waste, or cut carbon?",
        "Want a beginner plan you can start today?"
    ],
    "carbon_footprint": [
        "Want the biggest changes with the least effort?",
        "Do you want tips for travel, food, or home energy?"
    ],
    "renewable_energy": [
        "Want a simple comparison of solar vs wind vs hydro?",
        "Curious about renewable energy at home or just the basics?"
    ]
}

FALLBACKS = [
    "Hmm — I’m not 100% sure I got that. Can you rephrase it in a simpler way?",
    "I might be missing your point. Are you asking about climate change, pollution, recycling, or living sustainably?",
    "I didn’t catch that fully. Try asking it like you would to a friend — short and simple.",
    "Not totally sure. Give me one keyword (like ‘plastic’, ‘recycling’, ‘climate’) and I’ll jump in."
]

def get_response(user_input):
    """
    Get response from the chatbot based on user input
    """
    # If the configured model is a hosted LLM (model names that start with 'gpt-'),
    # forward the request to OpenAI (or other provider) instead of the local classifier.
    if MODEL_NAME and MODEL_NAME.lower().startswith('gpt'):
        try:
            return get_response_openai(user_input)
        except Exception as e:
            return {"text": f"Provider request failed: {str(e)}", "tag": "error", "confidence": 0.0}

    if model is None or intents_data is None:
        return {
            "text": "Sorry — my brain isn’t loaded right now. Please run `python train.py` and restart the server.",
            "tag": None,
            "confidence": 0.0
        }
    
    # Preprocess user input
    processed_input = preprocess_text(user_input)
    
    # Predict intent
    try:
        predicted_tag = model.predict([processed_input])[0]
        confidence = None

        # Confidence if available (Pipeline -> MultinomialNB supports predict_proba)
        try:
            proba = model.predict_proba([processed_input])[0]
            classes = list(model.classes_)
            confidence = float(proba[classes.index(predicted_tag)])
        except Exception:
            confidence = None

        # Confidence gate for fallback
        if confidence is not None and confidence < 0.30:
            return {
                "text": random.choice(FALLBACKS),
                "tag": "fallback",
                "confidence": confidence
            }

        base_response = None
        for intent in intents_data["intents"]:
            if intent["tag"] == predicted_tag:
                base_response = random.choice(intent["responses"])
                break

        if not base_response:
            return {
                "text": random.choice(FALLBACKS),
                "tag": "fallback",
                "confidence": confidence if confidence is not None else 0.0
            }

        # Humanize: small opener + occasional follow-up
        opener = random.choice(HUMAN_OPENERS)
        add_followup = random.random() < 0.45
        followup = ""
        if add_followup:
            followups = FOLLOW_UPS.get(predicted_tag, [])
            if followups:
                followup = " " + random.choice(followups)

        # Avoid double punctuation awkwardness
        text = f"{opener} {base_response}".strip()
        if followup:
            text = (text.rstrip() + "\n\n" + followup.strip()).strip()

        return {
            "text": text,
            "tag": predicted_tag,
            "confidence": confidence if confidence is not None else 1.0
        }
    
    except Exception as e:
        return {
            "text": f"Sorry — something went wrong on my side: {str(e)}",
            "tag": "error",
            "confidence": 0.0
        }


def get_response_openai(user_input):
    """
    Send the user input to an OpenAI-compatible chat model (e.g., 'gpt-5-mini').
    Requires `OPENAI_API_KEY` env var to be set when using provider models.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')

    system_prompt = (
        "You are an assistant specialized in environmental awareness."
        " Answer concisely and helpfully, focusing on sustainability, recycling, pollution, and climate topics."
    )

    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=300,
        temperature=0.7
    )

    # Extract assistant text
    text = ''
    try:
        text = resp['choices'][0]['message']['content'].strip()
    except Exception:
        text = str(resp)

    return {"text": text, "tag": "provider", "confidence": 1.0}

@app.route('/')
def index():
    """
    Serve the main chat interface
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Get response from the model
        result = get_response(user_message)
        
        # Get current timestamp
        timestamp = datetime.now().strftime('%H:%M')
        
        return jsonify({
            'success': True,
            'response': result["text"],
            'timestamp': timestamp,
            'tag': result.get("tag"),
            'confidence': result.get("confidence")
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    model_loaded = model is not None and intents_data is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Environmental Awareness Chatbot - Starting Server")
    print("=" * 50)
    
    # Load model on startup
    success, message = load_model()
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        print("Please run 'python train.py' to train the model first.")
    
    print("=" * 50)
    print("Server starting on http://127.0.0.1:5000")
    print("=" * 50)
    
    if __name__ == '__main__':
        # Load model on startup
        success, message = load_model()
        print(message)

        app.run(host='0.0.0.0', port=5000)

