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
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data received")
        
        # Log the received JSON data
        print(f"Received data: {data}")

        campaign_id = data.get('campaign_id')
        email_stats_id = data.get('stats_id')
        email_body = data.get('email_body')

        if not campaign_id or not email_stats_id or not email_body:
            raise ValueError("Missing required fields: campaign_id, stats_id, email_body")

        print(f"Parsed campaign_id: {campaign_id}, email_stats_id: {email_stats_id}, email_body: {email_body}")

        # Construct the data to send to the webhook
        webhook_data = {
            "campaign_id": campaign_id,
            "email_stats_id": email_stats_id,
            "email_body": email_body
        }

        # Send the POST request to the webhook URL
        response = requests.post(WEBHOOK_URL, json=webhook_data)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        return jsonify({"status": "success", "message": "Webhook triggered successfully"}), 200

    except requests.exceptions.RequestException as e:
        # Log the error and response
        print(f"Error: {e}")
        if e.response is not None:
            print(f"Response Content: {e.response.content}")
        return jsonify({"status": "error", "message": "Failed to trigger webhook", "details": str(e)}), 500

    except ValueError as e:
        # Log the error for missing fields or no JSON data
        print(f"ValueError: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        # Log any other exceptions
        print(f"Unexpected Error: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
Updated index.html
Make sure the form data is being correctly collected and sent to the server.

html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webhook Trigger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 400px;
            width: 100%;
            padding: 20px;
            background: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"], input[type="submit"], textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        .success-message {
            display: none;
            color: green;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Webhook Trigger</h1>
        <form id="webhookForm">
            <label for="campaign_id">Campaign ID:</label>
            <input type="text" id="campaign_id" name="campaign_id" required>
            <label for="stats_id">Email Stats ID:</label>
            <input type="text" id="stats_id" name="stats_id" required>
            <label for="email_body">Email Body:</label>
            <textarea id="email_body" name="email_body" rows="4" required></textarea>
            <input type="submit" value="Trigger Webhook">
        </form>
        <div class="success-message" id="successMessage">Webhook triggered successfully!</div>
    </div>

    <script>
        document.getElementById('webhookForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent form from submitting the traditional way

            const campaignId = document.getElementById('campaign_id').value;
            const statsId = document.getElementById('stats_id').value;
            const emailBody = document.getElementById('email_body').value;

            fetch('/trigger-webhook', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    campaign_id: campaignId,
                    stats_id: statsId,
                    email_body: emailBody
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const successMessage = document.getElementById('successMessage');
                    successMessage.style.display = 'block';
                    setTimeout(() => {
                        successMessage.style.display = 'none';
                        window.location.reload(); // Refresh the page
                    }, 2000); // Show success message for 2 seconds
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to trigger webhook.');
            });
        });
    </script>
</body>
</html>
