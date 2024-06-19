from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trigger-webhook', methods=['POST'])
def trigger_webhook():
    webhook_url = request.form.get('webhook_url')
    lead_id = request.form.get('lead_id')

    # Construct the data to send to the webhook
    data = {"lead_id": lead_id}

    # Send the POST request to the webhook URL
    response = requests.post(webhook_url, json=data)

    # Check the response from the webhook and return an appropriate message
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Webhook triggered successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to trigger webhook"}), response.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
