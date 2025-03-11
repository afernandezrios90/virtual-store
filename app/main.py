from flask import Flask, jsonify, request
import random
import logging
import time

app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Product simulation
PRODUCTS = [
    {"id": 1, "name": "Tshirt", "price": 25},
    {"id": 2, "name": "Jeans", "price": 70},
    {"id": 3, "name": "Socks", "price": 15},
]

# Timers for requests
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request_time(response):
    duration = time.time() - request.start_time
    log_data = {
        "client_ip": request.remote_addr,
        "path": request.path,
        "method": request.method,
        "status_code": response.status_code,
        "duration": f"{duration:.4f}s"
    }
    logging.info("Request from %(client_ip)s to %(path)s with %(method)s method responded with %(status_code)s in %(duration)s", log_data)
    return response

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Virtual Store!"})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(PRODUCTS)

@app.route('/buy/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    order_id = random.randint(1000, 9999)
    return jsonify({"message": "Purchase successful", "order_id": order_id, "product": product})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
