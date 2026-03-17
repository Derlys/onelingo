from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.getenv("HF_TOKEN")


import time
import random

@app.route('/api/challenge')
def get_challenge():

    topics = ["travel", "food", "hobbies", "work", "family", "movies", "nature"]
    chosen_topic = random.choice(topics)


    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a creative English teacher. Generate a UNIQUE A2 English challenge about {chosen_topic}.
    Return ONLY a JSON object. No intro.
    Example: {{"type":"reading","question":"Translate:","content":"I love traveling","options":["Me encanta viajar","No viajo","Como mucho"],"answer":0}}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    Generate a new challenge. Seed: {time.time()}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.9,
            "top_p": 0.95,
            "do_sample": True
        }
    }


# 2. RUTA RAÍZ
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=7860, debug=False)