
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Instagram Proxy is running!'

@app.route('/download_instagram', methods=['POST'])
def download_instagram():
    data = request.get_json()
    insta_url = data.get("url")

    try:
        api_url = "https://snapinsta.to/api/ajaxSearch"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = f"q={insta_url}&t=media"

        snapinsta_resp = requests.post(api_url, headers=headers, data=payload, timeout=10)
        result = snapinsta_resp.json()
        if result.get("data"):
            return jsonify({"url": result["data"][0]["url"]})
        return jsonify({"error": "No video found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
