"""
Model Training Script for Environmental Awareness Chatbot
Uses NLTK and scikit-learn to train a Naive Bayes classifier
"""

import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import nltk
from nltk.stem import PorterStemmer
import re
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except (LookupError, OSError):
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass  # Will fail gracefully if punkt can't be downloaded

# Initialize stemmer
stemmer = PorterStemmer()

def preprocess_text(text):
    """
    Preprocess text: convert to lowercase, remove special characters,
    and apply stemming
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize and stem
    words = nltk.word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed_words)

def load_intents(file_path='intents.json'):
    """
    Load intents from JSON file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def prepare_training_data(intents_data):
    """
    Prepare training data from intents
    Returns: X (patterns), y (tags)
    """
    X = []
    y = []
    
    for intent in intents_data['intents']:
        tag = intent['tag']
        for pattern in intent['patterns']:
            # Preprocess pattern
            processed_pattern = preprocess_text(pattern)
            X.append(processed_pattern)
            y.append(tag)
    
    return X, y

def train_model():
    """
    Train the Naive Bayes classifier
    """
    print("Loading intents data...")
    intents_data = load_intents()
    
    print("Preparing training data...")
    X, y = prepare_training_data(intents_data)
    
    print(f"Training on {len(X)} samples...")
    
    # Create pipeline with CountVectorizer and MultinomialNB
    model = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])
    
    # Train the model
    model.fit(X, y)
    
    print("Model trained successfully!")
    
    # Save the model
    model_path = 'model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")
    
    # Save intents data for response retrieval
    intents_path = 'intents_data.pkl'
    with open(intents_path, 'wb') as f:
        pickle.dump(intents_data, f)
    
    print(f"Intents data saved to {intents_path}")
    
    return model, intents_data

if __name__ == '__main__':
    print("=" * 50)
    print("Environmental Awareness Chatbot - Model Training")
    print("=" * 50)
    train_model()
    print("=" * 50)
    print("Training completed!")

