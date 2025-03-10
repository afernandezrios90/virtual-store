from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Product simulation
PRODUCTS = [
    {"id": 1, "name": "Tshirt", "price": 25},
    {"id": 2, "name": "Jeans", "price": 70},
    {"id": 3, "name": "Socks", "price": 15},
]

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
