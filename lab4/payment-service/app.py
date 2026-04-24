from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"service": "payment-service", "status": "up"})

@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json()

    amount = data.get("amount")

    return jsonify({
        "message": "Payment successful",
        "paid_amount": amount
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)