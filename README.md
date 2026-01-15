# 🌱 Environmental Awareness Chatbot

A fully interactive AI-powered web application that educates users about environmental issues such as climate change, pollution, recycling, and sustainable living.

## 🚀 Features
- **Interactive Chat Interface**: Modern, responsive chat UI with message bubbles
- **AI-Powered Responses**: Uses Naive Bayes classifier with NLTK and scikit-learn
- **Environmental Topics**: Covers climate change, pollution, recycling, sustainable living, and more
- **Real-time Communication**: AJAX/Fetch API for seamless chat experience
- **Typing Animation**: Visual feedback when bot is processing
- **Timestamps**: Each message includes a timestamp
- **Mobile Responsive**: Works perfectly on all device sizes
- **Eco-friendly Theme**: Beautiful green color scheme

## 📋 Prerequisites

- Python 3.7 or higher

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   ```

3. **Train the AI model**:
   ```bash
   python train.py
   ```
   This will create `model.pkl` and `intents_data.pkl` files.

## 🎯 Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **Start chatting!** Ask questions about:
   - Climate change
   - Pollution
   - Recycling
   - Sustainable living
   - Water conservation
   - Renewable energy
   - And more!

## 📁 Project Structure

```
Ai Environmenta Chatbot/
│
├── app.py                 # Flask backend server
├── train.py              # Model training script
├── intents.json          # Training dataset
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
├── templates/
│   └── index.html       # Main chat interface
│
└── static/
    ├── style.css        # Eco-friendly styling
    └── script.js        # Frontend JavaScript logic
```

## 🔧 Technical Details

### Backend
- **Framework**: Flask
- **ML Model**: Naive Bayes Classifier (MultinomialNB)
- **NLP**: NLTK for text preprocessing and tokenization
- **Vectorization**: CountVectorizer from scikit-learn
- **Text Processing**: Porter Stemmer for word stemming

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Vanilla JS (no frameworks)
- **API Communication**: Fetch API

## 🎨 UI Features

- Clean, modern design with eco-friendly green theme
- Rounded chat bubbles for user and bot messages
- Smooth animations and transitions
- Typing indicator animation
- Responsive layout for mobile and desktop
- Auto-scrolling chat window
- Welcome message on page load

## 📝 Example Questions

Try asking:
- "What is climate change?"
- "How can I reduce pollution?"
- "Tell me about recycling"
- "What is sustainable living?"
- "How to save water?"
- "Explain renewable energy"

## 🔄 Model Training

The model is trained using:
- **Algorithm**: Multinomial Naive Bayes
- **Features**: Count-based vectorization
- **Preprocessing**: Lowercasing, special character removal, stemming

To retrain the model with new data:
1. Update `intents.json` with new patterns and responses
2. Run `python train.py` again

## 🐛 Troubleshooting

**Model not found error:**
- Make sure you've run `python train.py` before starting the server

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Port already in use:**
- Change the port in `app.py` (line 120) from 5000 to another port

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to expand the intents dataset in `intents.json` to add more environmental topics and responses!

## 🌍 Impact

This chatbot helps raise awareness about environmental issues and encourages sustainable practices. Every conversation can inspire positive change!

---

Made with ❤️ for a sustainable future 🌱

