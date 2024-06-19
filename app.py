from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook Trigger App is Running"

@app.route('/trigger-webhook', methods=['POST'])
def trigger_webhook():
    webhook_url = request.json.get('webhook_url')
    data = request.json.get('data', {})

    response = requests.post(webhook_url, json=data)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Webhook triggered successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to trigger webhook"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
