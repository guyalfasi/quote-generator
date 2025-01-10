import json
from flask import Flask, request, send_file
from image_gen import generate_image

app = Flask(__name__)

# Load data
with open('data/quotes.json', 'r') as f:
    quotes = json.load(f)

with open('data/characters.json', 'r') as f:
    characters = json.load(f)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data:
        return "Missing JSON payload", 400

    # Extract character and quote from the payload
    character_name = data.get('character')
    quote = data.get('quote')

    # Validate input
    if not character_name or not quote:
        return "Missing character or quote", 400

    # Find the character object in the list
    character = next((c for c in characters if c['name'] == character_name), None)
    if not character:
        return "Invalid character", 400

    # Generate the image
    try:
        return generate_image(character, quote)
    except Exception as e:
        return f"Error generating image: {str(e)}", 500


if __name__ == '__main__':
    app.run()
