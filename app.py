from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = "https://getonapod.app.n8n.cloud/webhook-test/f07486db-a7db-4f96-91cc-765809309105"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trigger-webhook', methods=['POST'])
def trigger_webhook():
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    message_id = data.get('message_id')
    stats_id = data.get('stats_id')

    print(f"Received campaign_id: {campaign_id}, message_id: {message_id}, stats_id: {stats_id}")

    # Construct the data to send to the webhook
    webhook_data = {
        "campaign_id": campaign_id,
        "message_id": message_id,
        "stats_id": stats_id
    }

    # Send the POST request to the webhook URL
    try:
        response = requests.post(WEBHOOK_URL, json=webhook_data)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return jsonify({"status": "success", "message": "Webhook triggered successfully"}), 200
    except requests.exceptions.RequestException as e:
        # Log the error and response
        print(f"Error: {e}")
        if response is not None:
            print(f"Response Content: {response.content}")
        return jsonify({"status": "error", "message": "Failed to trigger webhook", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
