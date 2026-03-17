from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests
import time
import random

app = Flask(__name__, static_folder='.')
CORS(app)

# Configuración de variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")
# Usamos Llama-3 para mayor calidad y velocidad
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

@app.route('/api/challenge')
def get_challenge():
    topics = ["travel", "food", "hobbies", "work", "family", "movies", "nature"]
    chosen_topic = random.choice(topics)

    # Prompt diseñado para evitar repeticiones y asegurar formato JSON
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a creative English teacher. Generate a UNIQUE A2 English challenge about {chosen_topic}.
    Return ONLY a JSON object. No intro.
    Example: {{"type":"reading","question":"Translate:","content":"I love traveling","options":["Me encanta viajar","No viajo","Como mucho"],"answer":0}}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    Generate a new challenge. Seed: {time.time()}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>"""

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.8,
            "do_sample": True
        }
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_ID}",
            headers=headers,
            json=payload,
            timeout=10
        )
        result = response.json()

        # Lógica para extraer solo el JSON de la respuesta de la IA
        if isinstance(result, list):
            raw_text = result[0]['generated_text']
        else:
            raw_text = result.get('generated_text', '')

        clean_text = raw_text.split("<|assistant|>")[-1].strip()
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        return clean_text[start:end]

    except Exception as e:
        print(f"Error: {e}")
        # Fallback por si la IA falla o tarda mucho
        return jsonify({
            "type": "reading",
            "question": "Translate:",
            "content": "Learning English is fun",
            "options": ["Aprender inglés es divertido", "El sol es frío", "No sé"],
            "answer": 0
        })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Railway requiere que usemos el puerto dinámico asignado
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port, debug=False)