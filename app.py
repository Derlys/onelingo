from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from groq import Groq
import os
import random

app = Flask(__name__, static_folder='.')
CORS(app)


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/challenge')
def get_challenge():
    topics = ["travel", "food", "hobbies", "work", "family", "movies", "nature"]
    chosen_topic = random.choice(topics)

    try:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative English teacher. Return ONLY a JSON object for an A2 English challenge. No intro text."
                },
                {
                    "role": "user",
                    "content": f"Generate a challenge about {chosen_topic}. Format: {{\"type\":\"reading\",\"question\":\"Translate:\",\"content\":\"...\",\"options\":[\"...\"],\"answer\":0}}"
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"} #
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error en Groq: {e}")
        return jsonify({"error": "No se pudo generar el reto"}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)