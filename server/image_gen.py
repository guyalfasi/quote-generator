import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from io import BytesIO
from uuid import uuid4
import random

with open('data/quotes.json', 'r') as f:
    quotes = json.load(f)

with open('data/characters.json', 'r') as f:
    characters = json.load(f)

font_path = "static/fonts/ShadowsIntoLight-Regular.ttf"
image_dir = "static/images/"

def scale_character(char_size):
    char_width, char_height = char_size
    max_width, max_height = 640, 720

    scale = min(max_width / char_width, max_height / char_height)
    
    return (int(char_width * scale), int(char_height * scale))

def generate_image(character, quote):
    quote_img = Image.new("RGB", (1280, 720))

    image_path = os.path.join(image_dir, character["img"])
    char_img = Image.open(image_path)
    char_img = char_img.resize(scale_character(char_img.size))
    char_img_grayscaled = ImageOps.grayscale(char_img)

    quote_img.paste(char_img_grayscaled, (0, 180))

    font = ImageFont.truetype(font_path, 48)
    draw = ImageDraw.Draw(quote_img)
    draw.text((640, 100), quote, (255, 255, 255), font=font, anchor="mm")
    draw.text((640, 400), f"- {character['name']}", (255, 255, 255), font=font, anchor="mm")

    img_io = BytesIO()
    quote_img.save(img_io, "PNG")
    img_io.seek(0) 
    
    return img_io

if __name__ == '__main__':
    char = next((c for c in characters if c['name'] == 'Goku'), None)
    print(generate_image(char, random.choice(quotes)))
