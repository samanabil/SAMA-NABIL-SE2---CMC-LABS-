import os
import time
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:5001"
)

# 👉 NEW: payment service URL
PAYMENT_SERVICE_URL = "http://payment-service:5003"


def fetch_product(product_id, retries=2, delay=1):
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"

    for attempt in range(retries + 1):
        try:
            return requests.get(url, timeout=2)
        except:
            if attempt < retries:
                time.sleep(delay)
            else:
                return None


# 👉 NEW FUNCTION (payment call)
def make_payment(amount):
    try:
        return requests.post(
            f"{PAYMENT_SERVICE_URL}/pay",
            json={"amount": amount},
            timeout=2
        )
    except:
        return None


@app.route("/health")
def health():
    return jsonify({"service": "order-service", "status": "up"})


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    response = fetch_product(product_id)

    if response is None:
        return jsonify({"error": "product-service unavailable"}), 503

    if response.status_code != 200:
        return jsonify({"error": "invalid product"}), 400

    product = response.json()
    total = product["price"] * quantity

    # 👉 NEW: call payment service
    payment_response = make_payment(total)

    if payment_response is None:
        return jsonify({"error": "payment service failed"}), 503

    return jsonify({
        "message": "Order created + paid",
        "product": product["name"],
        "quantity": quantity,
        "total_price": total,
        "payment_status": payment_response.json()
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)