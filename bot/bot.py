import nltk
import re
import json
from datetime import datetime

class EcommerceBot:
    def __init__(self):
        self.products = []
        self.cart = []
        self.current_session = {}
        
        # Bot responses template
        self.responses = {
            'greeting': [
                "Hello! Welcome to our store! How can I help you today?",
                "Hi there! Ready to shop? What are you looking for?",
                "Welcome! How can I assist you with your shopping?"
            ],
            'product_inquiry': [
                "I found these products for you:",
                "Here are some items that match your search:",
                "Check out these products:"
            ],
            'order_help': [
                "I can help you place an order! What would you like to buy?",
                "Let me help you with your order. What products are you interested in?",
                "Ready to order? Tell me what you need!"
            ],
            'payment_info': [
                "We accept cash on delivery, bKash, Nagad, and credit cards.",
                "Payment options: COD, mobile banking, and card payments.",
                "You can pay via cash, bKash, Nagad, or credit card."
            ]
        }
    
    def process_message(self, message):
        message = message.lower()
        
        # Greeting detection
        if any(word in message for word in ['hello', 'hi', 'hey', 'hola']):
            return self.get_response('greeting')
        
        # Product search
        elif any(word in message for word in ['product', 'item', 'buy', 'purchase', 'price']):
            return self.handle_product_search(message)
        
        # Order related
        elif any(word in message for word in ['order', 'cart', 'checkout']):
            return self.handle_order_request(message)
        
        # Payment related
        elif any(word in message for word in ['payment', 'pay', 'money', 'price']):
            return self.get_response('payment_info')
        
        else:
            return "I'm here to help with your shopping! You can ask me about products, prices, or place orders."

    def handle_product_search(self, message):
        # Extract product keywords
        keywords = re.findall(r'\b(shirt|pant|shoe|watch|phone|laptop|book)\b', message)
        
        if keywords:
            return f"Looking for {keywords[0]}? I can show you our {keywords[0]} collection!"
        else:
            return "What type of products are you looking for? (e.g., shirts, electronics, books)"

    def handle_order_request(self, message):
        if 'place' in message or 'create' in message:
            return "Great! To place an order, please tell me what products you want and your contact information."
        elif 'status' in message:
            return "To check your order status, please provide your order ID."
        else:
            return self.get_response('order_help')
    
    def get_response(self, response_type):
        import random
        return random.choice(self.responses[response_type])

# Initialize bot
bot = EcommerceBot()
