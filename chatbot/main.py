import re
from datetime import datetime
from typing import Dict, List, Tuple
import json
import random

class EnhancedChatbot:
    def __init__(self):
        self.conversation_history: List[Tuple[str, str]] = []
        self.patterns: Dict[str, List[str]] = {
            'greetings': [
                r'\b(hi|hello|hey|good\s*(morning|afternoon|evening))\b',
                "Hello! How can I help you today?|Hi there! What can I do for you?|Hey! Nice to meet you!"
            ],
            'farewell': [
                r'\b(bye|goodbye|see\s*you|take\s*care)\b',
                "Goodbye! Have a great day!|Take care! Come back soon!|Bye! It was nice chatting with you!"
            ],
            'gratitude': [
                r'\b(thanks|thank\s*you|appreciate\s*it)\b',
                "You're welcome!|Glad I could help!|No problem at all!"
            ],
            'about': [
                r'\b(who|what).+\b(you|your\s*name)\b',
                "I'm an AI chatbot designed to help you!|I'm your friendly virtual assistant!"
            ],
            'time': [
                r'\b(what|current)\s*(time|hour)\b',
                lambda: f"It's {datetime.now().strftime('%I:%M %p')} right now."
            ],
            'mood': [
                r'how\s*(are|re|is).+(you|going|doing)\b',
                "I'm doing great, thanks for asking! How about you?|I'm excellent! How are you today?"
            ]
        }
        
    def preprocess_input(self, user_input: str) -> str:
        return user_input.lower().strip()
    
    def get_response(self, pattern: str, responses: str) -> str:
        if callable(responses):
            return responses()
        return random.choice(responses.split("|"))
    
    def find_best_match(self, user_input: str) -> str:
        for category, (pattern, responses) in self.patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return self.get_response(pattern, responses)
        
        # Context-aware fallback responses
        if len(self.conversation_history) > 0:
            last_user_input = self.conversation_history[-1][0]
            if re.search(r'\b(yes|yeah|yep)\b', user_input):
                return "That's great! What else would you like to know?"
            elif re.search(r'\b(no|nope|nah)\b', user_input):
                return "I see. Is there something else I can help you with?"
        
        return "I'm not sure I understand. Could you rephrase that or ask something else?"
    
    def chat(self, user_input: str) -> str:
        processed_input = self.preprocess_input(user_input)
        response = self.find_best_match(processed_input)
        self.conversation_history.append((processed_input, response))
        return response

# Flask server implementation
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
chatbot = EnhancedChatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = chatbot.chat(user_input)
    return jsonify({
        "response": response,
        "timestamp": datetime.now().strftime("%H:%M")
    })

if __name__ == "__main__":
    app.run(debug=True)