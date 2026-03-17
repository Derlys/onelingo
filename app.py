from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from groq import Groq
import os
import random

app = Flask(__name__, static_folder='.')
CORS(app)

# Cliente de Groq - Asegúrate de poner GROQ_API_KEY en las variables de Railway
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/challenge')
def get_challenge():
    topics = ["travel", "food", "hobbies", "work", "family", "movies", "nature"]
    chosen_topic = random.choice(topics)

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are an English teacher. Return ONLY a JSON object for an A2 challenge. No intro."
                },
                {
                    "role": "user",
                    "content": f"Topic: {chosen_topic}. Format: {{\"type\":\"reading\",\"question\":\"Translate:\",\"content\":\"...\",\"options\":[\"...\"],\"answer\":0}}"
                }
            ],
            response_format={"type": "json_object"}
        )

        # Aquí está el return que le faltaba a tu log
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error detectado: {e}")
        # Respuesta de respaldo para que la app nunca se caiga
        return jsonify({
            "type": "reading",
            "question": "Translate:",
            "content": "I want to learn more English",
            "options": ["Quiero aprender más inglés", "Me gusta el café", "Tengo sueño"],
            "answer": 0
        })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)