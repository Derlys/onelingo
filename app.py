from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import requests
import random

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/api/challenge')
def get_challenge():
    api_key = os.environ.get("GROQ_API_KEY")
    topics = ["travel", "food", "hobbies", "work", "family", "movies", "nature"]
    chosen_topic = random.choice(topics)

    # URL directa de la API de Groq
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Return ONLY a JSON object for an A2 English challenge. No intro."},
            {"role": "user", "content": f"Topic: {chosen_topic}. Format: {{\"question\":\"Translate:\",\"content\":\"...\",\"options\":[\"...\"],\"answer\":0}}"}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            print(f"Respuesta de Groq: {response.status_code} - {response.text}")

            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        except Exception as e:
            print(f"ERROR DETALLADO: {e}")
            return jsonify({"error": "Falló la conexión con la IA"}), 500
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)