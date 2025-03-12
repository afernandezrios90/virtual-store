from flask import Flask, jsonify, request
import random
import logging
import time
import psutil
from prometheus_client import Counter, Summary, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

###### Telemetry data generation ######

# Metrics configuration
CPU_USAGE = Gauge("app_cpu_usage_percent", "Percentage CPU usage", ["container"])
MEMORY_USAGE = Gauge("app_memory_usage_bytes", "Memory usage of the container", ["container"])
# Note: Summary generates both metrics for request count and duration (count and sum)
REQUEST_LATENCY = Summary("app_requests_duration_milliseconds", "Total request duration in milliseconds", ["response_code", "endpoint"])

# Functions to get container metrics
def get_container_memory_usage():
    try:
        with open("/sys/fs/cgroup/memory/memory.usage_in_bytes", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return psutil.virtual_memory().used  # Fallback if not running in a container

def get_container_name():
    # Return content of file /etc/hostname
    try:
        with open("/etc/hostname", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

###### Store content setup ######

# Product simulation
PRODUCTS = [
    {"id": 1, "name": "Tshirt", "price": 25},
    {"id": 2, "name": "Jeans", "price": 70},
    {"id": 3, "name": "Socks", "price": 15},
]

###### Request handling ######

# Before processing any incoming request, start the timer
@app.before_request
def start_timer():
    request.start_time = time.time()

# After processing any incoming request, register telemetry data
@app.after_request
def log_request_time(response):
    # Calculate response time
    duration = (time.time() - request.start_time) * 1000
    # Increment request counters
    REQUEST_LATENCY.labels(response.status_code, request.path).observe(duration)
    # Log request
    log_data = {
        "client_ip": request.remote_addr,
        "path": request.path,
        "method": request.method,
        "status_code": response.status_code,
        "duration": f"{duration:.4f}s"
    }
    logging.info("Request from %(client_ip)s to %(path)s with %(method)s method responded with %(status_code)s in %(duration)s", log_data)
    return response

@app.route('/', methods=['GET'])
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

# Metrics endpoint
@app.route('/metrics')
def metrics():
    # Update metrics in real-time
    CPU_USAGE.labels(get_container_name()).set(round(random.uniform(0.1, 0.4), 5))
    MEMORY_USAGE.labels(get_container_name()).set(get_container_memory_usage())
    # Expose last values
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
