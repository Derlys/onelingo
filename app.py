from flask import Flask, send_from_directory, jsonify
import os, requests, random
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/api/challenge')
def get_challenge():
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": "Generate one A2 English quiz in JSON: {question, content, options, answer}"}],
            "response_format": {"type": "json_object"}
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.text # Enviamos directamente lo que diga Groq
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)