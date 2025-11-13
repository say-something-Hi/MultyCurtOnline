from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os
import logging
from bot.bot import EcommerceBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize bot
bot = EcommerceBot()

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'ecommerce.db')

def get_db_connection():
    """Get database connection"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            stock INTEGER,
            category TEXT,
            image_url TEXT
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_phone TEXT,
            customer_address TEXT,
            products TEXT,  # JSON string of products
            total_amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            product_id INTEGER,
            quantity INTEGER,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample products if table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Men\'s T-Shirt', 899, 'Comfortable cotton t-shirt', 50, 'clothing', '/images/tshirt.jpg'),
            ('Wireless Headphones', 2499, 'Noise cancelling headphones', 25, 'electronics', '/images/headphones.jpg'),
            ('Smart Watch', 3999, 'Fitness tracking smartwatch', 30, 'electronics', '/images/smartwatch.jpg'),
            ('Running Shoes', 1999, 'Comfortable running shoes', 40, 'footwear', '/images/shoes.jpg'),
            ('Backpack', 1299, 'Waterproof laptop backpack', 35, 'accessories', '/images/backpack.jpg')
        ]
        cursor.executemany('''
            INSERT INTO products (name, price, description, stock, category, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_products)
        logger.info("Sample products inserted")
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

@app.route('/')
def home():
    return jsonify({
        "message": "Ecommerce Bot API is running!",
        "status": "success",
        "endpoints": {
            "products": "/api/products",
            "create_order": "/api/orders",
            "bot_chat": "/api/bot/chat"
        }
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        
        product_list = []
        for product in products:
            product_list.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'description': product[3],
                'stock': product[4],
                'category': product[5],
                'image_url': product[6]
            })
        
        return jsonify({
            "status": "success",
            "data": product_list
        })
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.json
        logger.info(f"Creating order: {data}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (customer_name, customer_phone, customer_address, products, total_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['customer_name'], 
            data['customer_phone'],
            data.get('customer_address', ''),
            json.dumps(data['products']), 
            data['total_amount']
        ))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success",
            "order_id": order_id, 
            "message": "Order created successfully!"
        })
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/bot/chat', methods=['POST'])
def bot_chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"status": "error", "message": "No message provided"}), 400
        
        # Process message with bot
        bot_response = bot.process_message(user_message)
        
        return jsonify({
            "status": "success",
            "response": bot_response,
            "user_message": user_message
        })
    except Exception as e:
        logger.error(f"Error in bot chat: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "ecommerce-bot"})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
