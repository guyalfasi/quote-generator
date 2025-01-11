import json
import random
from flask import Flask, jsonify, request, send_file
from image_gen import generate_image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load data
with open('data/quotes.json', 'r') as f:
    quotes = json.load(f)

@app.route('/characters', methods=['GET'])
def get_characters():
    with open('data/characters.json', 'r') as f:
        characters = json.load(f)
    return jsonify(characters)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    character_name = data.get('character')
    quote = data.get('quote')

    if not character_name:
        return jsonify({"error": "Missing character"}), 400

    with open('data/characters.json', 'r') as f:
        characters = json.load(f)

    character = next((c for c in characters if c['name'] == character_name), None)
    if not character:
        return jsonify({"error": "Invalid character"}), 400

    try:
        image_stream = generate_image(character, quote if quote else random.choice(quotes))
        return send_file(image_stream, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": f"Error generating image: {str(e)}"}), 500


if __name__ == '__main__':
    app.run()

