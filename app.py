from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = "https://getonapod.app.n8n.cloud/webhook-test/a06606f6-d5ba-47d1-a6e8-73c24f8d45f6"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trigger-webhook', methods=['POST'])
def trigger_webhook():
    lead_id = request.form.get('lead_id')
    print(f"Received lead_id: {lead_id}")

    # Construct the data to send to the webhook
    data = {"lead_id": lead_id}

    # Send the POST request to the webhook URL
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
    except requests.exceptions.RequestException as e:
        # Log the error and response
        print(f"Error: {e}")
        if response is not None:
            print(f"Response Content: {response.content}")
        return jsonify({"status": "error", "message": "Failed to trigger webhook", "details": str(e)}), 500

    # Check the response from the webhook and return an appropriate message
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Webhook triggered successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to trigger webhook", "details": response.content.decode()}), response.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
