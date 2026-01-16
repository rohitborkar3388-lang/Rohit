/**
 * Environmental Awareness Chatbot - Frontend JavaScript
 * Handles chat interface, API communication, and UI interactions
 */

// DOM Elements
const chatWindow = document.getElementById('chatWindow');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const botStatus = document.getElementById('botStatus');
const statusDot = document.getElementById('statusDot');
const quickChips = document.getElementById('quickChips');
const clearChatBtn = document.getElementById('clearChatBtn');
const channelTitle = document.getElementById('channelTitle');

const DEFAULT_CHIPS = [
    { label: "What’s climate change?", text: "what’s climate change?" },
    { label: "How do I recycle right?", text: "how do i recycle properly?" },
    { label: "Tips to reduce plastic", text: "how to reduce plastic waste?" },
    { label: "Sustainable living ideas", text: "give me sustainable living tips" },
    { label: "How to save water?", text: "how can i save water at home?" },
    { label: "Carbon footprint help", text: "how do i reduce my carbon footprint?" }
];

// Initialize welcome message timestamp
document.addEventListener('DOMContentLoaded', () => {
    const welcomeTimestamp = document.getElementById('welcomeTimestamp');
    if (welcomeTimestamp) {
        welcomeTimestamp.textContent = getCurrentTime();
    }
    initDiscordLike();
    renderChips(DEFAULT_CHIPS);
});

/**
 * Get current time in HH:MM format
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
    });
}

function initDiscordLike() {
    // Seed a welcome message in the log
    if (chatWindow && chatWindow.children.length === 0) {
        addDiscordMessage({
            author: "EcoChat",
            role: "bot",
            text: "Hey! Welcome to #general. Ask me anything about climate change, pollution, recycling, or sustainable living.",
            timestamp: getCurrentTime()
        });
    }

    // Wire channel buttons
    const channels = document.querySelectorAll('.channel');
    channels.forEach((btn) => {
        btn.addEventListener('click', () => {
            channels.forEach((b) => b.classList.remove('active'));
            btn.classList.add('active');
            const topic = btn.getAttribute('data-topic') || 'general';
            const name = btn.textContent.replace('#', '').trim();
            if (channelTitle) channelTitle.textContent = name;
            userInput.placeholder = `Message #${name}`;
            // Gentle context message
            addDiscordMessage({
                author: "EcoChat",
                role: "bot",
                text: `Switched to #${name}. What do you want to talk about here?`,
                timestamp: getCurrentTime()
            });
            renderChips(chipsForTopic(topic));
        });
    });
}

function chipsForTopic(topic) {
    const map = {
        general: DEFAULT_CHIPS,
        climate: [
            { label: "Why is it getting hotter?", text: "why is it getting hotter lately?" },
            { label: "Biggest climate causes?", text: "what causes climate change the most?" },
            { label: "What can I do?", text: "what can i do to help climate change?" }
        ],
        pollution: [
            { label: "Air pollution tips", text: "how can i reduce air pollution?" },
            { label: "Water pollution causes", text: "what causes water pollution?" },
            { label: "Plastic pollution", text: "why is plastic pollution so bad?" }
        ],
        recycling: [
            { label: "Recycle correctly", text: "how do i recycle properly?" },
            { label: "What goes in bin?", text: "what can be recycled?" },
            { label: "Recycling mistakes", text: "common recycling mistakes?" }
        ],
        sustainable: [
            { label: "Easy eco habits", text: "easy sustainable habits for beginners?" },
            { label: "Low-waste tips", text: "how to reduce waste at home?" },
            { label: "Eco-friendly lifestyle", text: "how to live more eco-friendly?" }
        ],
        plastic: [
            { label: "Cut single-use plastic", text: "how do i reduce single use plastic?" },
            { label: "Plastic alternatives", text: "what are good alternatives to plastic?" },
            { label: "Microplastics", text: "what are microplastics?" }
        ],
        water: [
            { label: "Save water at home", text: "how can i save water at home?" },
            { label: "Short shower tips", text: "easy ways to use less water?" },
            { label: "Why conserve water?", text: "why is water conservation important?" }
        ],
        energy: [
            { label: "Renewable energy basics", text: "what is renewable energy?" },
            { label: "Solar vs wind", text: "solar vs wind energy?" },
            { label: "Save electricity", text: "how to save electricity at home?" }
        ]
    };
    return map[topic] || DEFAULT_CHIPS;
}

function setBotStatus(text, mode = 'online') {
    if (botStatus) botStatus.textContent = text;
    if (statusDot) {
        statusDot.classList.toggle('typing', mode === 'typing');
    }
}

function renderChips(chips) {
    if (!quickChips) return;
    quickChips.innerHTML = '';

    chips.forEach((chip) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'chip';
        btn.textContent = chip.label;
        btn.addEventListener('click', () => {
            userInput.value = chip.text;
            sendButton.disabled = !userInput.value.trim();
            userInput.focus();
            sendMessage();
        });
        quickChips.appendChild(btn);
    });
}

/**
 * Add message to chat window
 */
function addDiscordMessage({ author, role, text, timestamp }) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role === 'bot' ? '🌿' : '🙂';
    messageDiv.appendChild(avatar);

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    const header = document.createElement('div');
    header.className = 'msg-header';

    const authorSpan = document.createElement('span');
    authorSpan.className = `author ${role}`;
    authorSpan.textContent = author;
    header.appendChild(authorSpan);

    const ts = document.createElement('span');
    ts.className = 'timestamp';
    ts.textContent = timestamp || getCurrentTime();
    header.appendChild(ts);

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const messageText = document.createElement('p');
    messageText.textContent = text;

    messageContent.appendChild(messageText);
    bubble.appendChild(header);
    bubble.appendChild(messageContent);
    messageDiv.appendChild(bubble);

    chatWindow.appendChild(messageDiv);
    scrollToBottom();
    return { messageDiv, messageText };
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message typing-message';
    typingDiv.id = 'typingIndicator';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = '🌿';
    typingDiv.appendChild(avatar);

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    const header = document.createElement('div');
    header.className = 'msg-header';
    const authorSpan = document.createElement('span');
    authorSpan.className = 'author bot';
    authorSpan.textContent = 'EcoChat';
    header.appendChild(authorSpan);
    const ts = document.createElement('span');
    ts.className = 'timestamp';
    ts.textContent = getCurrentTime();
    header.appendChild(ts);

    const typingContent = document.createElement('div');
    typingContent.className = 'typing-indicator';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        typingContent.appendChild(dot);
    }

    bubble.appendChild(header);
    bubble.appendChild(typingContent);
    typingDiv.appendChild(bubble);

    chatWindow.appendChild(typingDiv);
    scrollToBottom();
}

/**
 * Remove typing indicator
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Scroll chat window to bottom
 */
function scrollToBottom() {
    // Smooth-ish snap to bottom (prevents jitter while typing)
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

/**
 * Typewriter effect for bot reply
 */
async function typewriter(textNode, fullText, { minDelay = 8, maxDelay = 22 } = {}) {
    textNode.textContent = '';
    for (let i = 0; i < fullText.length; i++) {
        textNode.textContent += fullText[i];
        scrollToBottom();
        const delay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
        // Slightly pause at punctuation to feel more human
        const ch = fullText[i];
        const extra = (ch === '.' || ch === '!' || ch === '?' || ch === ',') ? 80 : 0;
        await new Promise((r) => setTimeout(r, delay + extra));
    }
}

/**
 * Send message to backend
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Disable input and button
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addDiscordMessage({
        author: "You",
        role: "user",
        text: message,
        timestamp: getCurrentTime()
    });
    
    // Clear input
    userInput.value = '';
    
    // Show typing indicator
    setBotStatus('Typing…', 'typing');
    showTypingIndicator();
    
    try {
        // Send request to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            // Add bot response with typewriter effect
            const { messageText } = addDiscordMessage({
                author: "EcoChat",
                role: "bot",
                text: "",
                timestamp: getCurrentTime()
            });
            await typewriter(messageText, data.response);
        } else {
            // Show error message
            addDiscordMessage({
                author: "EcoChat",
                role: "bot",
                text: "Sorry — I hit an error. Try again?",
                timestamp: getCurrentTime()
            });
            console.error('Error:', data.error);
        }
    } catch (error) {
        // Remove typing indicator
        removeTypingIndicator();
        
        // Show error message
        addDiscordMessage({
            author: "EcoChat",
            role: "bot",
            text: "I’m having trouble connecting right now. Can you try again in a sec?",
            timestamp: getCurrentTime()
        });
        console.error('Network error:', error);
    } finally {
        // Re-enable input and button
        setBotStatus('Online', 'online');
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

/**
 * Handle send button click
 */
sendButton.addEventListener('click', sendMessage);

/**
 * Handle Enter key press
 */
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

/**
 * Auto-focus input on load
 */
window.addEventListener('load', () => {
    userInput.focus();
});

/**
 * Handle input changes for better UX
 */
userInput.addEventListener('input', () => {
    // Enable/disable send button based on input
    if (userInput.value.trim()) {
        sendButton.disabled = false;
    } else {
        sendButton.disabled = true;
    }
});

// Initialize send button state
sendButton.disabled = true;

// Clear chat
if (clearChatBtn) {
    clearChatBtn.addEventListener('click', () => {
        const nodes = Array.from(chatWindow.querySelectorAll('.message'));
        nodes.forEach((n) => n.remove());
        addDiscordMessage({
            author: "EcoChat",
            role: "bot",
            text: "Fresh start! Ask me anything eco-related 🙂",
            timestamp: getCurrentTime()
        });
        renderChips(DEFAULT_CHIPS);
    });
}

