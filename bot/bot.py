import re
import json
import random
from datetime import datetime

class EcommerceBot:
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! Welcome to our store! How can I help you today? 👋",
                "Hi there! Ready to shop? What are you looking for? 🛍️",
                "Welcome! How can I assist you with your shopping? 😊"
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
                "We accept cash on delivery, bKash, Nagad, and credit cards. 💳",
                "Payment options: COD, mobile banking, and card payments. 📱",
                "You can pay via cash, bKash, Nagad, or credit card. 💰"
            ],
            'shipping_info': [
                "We offer free shipping for orders over ৳1000! 🚚",
                "Shipping takes 2-3 business days. Dhaka metro area: 1 day. ⏱️",
                "Free shipping on orders above ৳1000. Delivery time: 1-3 days. 📦"
            ]
        }
    
    def process_message(self, message):
        message = message.lower()
        
        # Greeting detection
        if any(word in message for word in ['hello', 'hi', 'hey', 'hola', 'start']):
            return self.get_response('greeting')
        
        # Product search
        elif any(word in message for word in ['product', 'item', 'buy', 'purchase', 'price', 'কিনতে']):
            return self.handle_product_search(message)
        
        # Order related
        elif any(word in message for word in ['order', 'cart', 'checkout', 'অর্ডার']):
            return self.handle_order_request(message)
        
        # Payment related
        elif any(word in message for word in ['payment', 'pay', 'money', 'price', 'পেমেন্ট']):
            return self.get_response('payment_info')
        
        # Shipping related
        elif any(word in message for word in ['shipping', 'delivery', 'ডেলিভারি']):
            return self.get_response('shipping_info')
        
        # Help
        elif any(word in message for word in ['help', 'সাহায্য']):
            return self.get_help_message()
        
        else:
            return "I'm here to help with your shopping! 🛒 You can ask me about products, prices, shipping, or place orders. Type 'help' for more options."

    def handle_product_search(self, message):
        categories = {
            'shirt': 'clothing',
            't-shirt': 'clothing', 
            'pant': 'clothing',
            'shoe': 'footwear',
            'watch': 'electronics',
            'headphone': 'electronics',
            'phone': 'electronics',
            'laptop': 'electronics',
            'book': 'books',
            'bag': 'accessories',
            'backpack': 'accessories'
        }
        
        for keyword, category in categories.items():
            if keyword in message:
                return f"Looking for {keyword}? 👕 I can show you our {category} collection! Check out the products above or tell me more about what you need."
        
        return "What type of products are you looking for? 🎯 (e.g., shirts, electronics, shoes, accessories)"

    def handle_order_request(self, message):
        if 'place' in message or 'create' in message or 'করব' in message:
            return "Great! To place an order: 1) Tell me what products you want 2) Your contact info 3) Delivery address. I'll guide you through the process! 📝"
        elif 'status' in message or 'স্ট্যাটাস' in message:
            return "To check your order status, please provide your order ID. You can also call us at 017XX-XXXXXX. 📞"
        else:
            return self.get_response('order_help')
    
    def get_help_message(self):
        help_text = """
🤖 **How I can help you:**

🛍️ **Product Inquiry**
- "Show me shirts"
- "What electronics do you have?"
- "Price of watches"

📦 **Order Management**  
- "I want to place an order"
- "How to checkout?"
- "Order status"

💳 **Payment & Shipping**
- "Payment methods"
- "Delivery time"
- "Shipping cost"

💬 Just ask me anything about shopping!
        """
        return help_text
    
    def get_response(self, response_type):
        return random.choice(self.responses[response_type])

# Initialize bot
bot = EcommerceBot()
