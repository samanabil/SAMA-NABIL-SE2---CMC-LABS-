from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "price": 1200},
    2: {"id": 2, "name": "Phone", "price": 650},
    3: {"id": 3, "name": "Headphones", "price": 120}
}

@app.route("/health")
def health():
    return jsonify({"service": "product-service", "status": "up"})

@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = PRODUCTS.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001) 