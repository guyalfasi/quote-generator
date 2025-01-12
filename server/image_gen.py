import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from io import BytesIO
import random
from typing import List, Dict
import textwrap

with open('data/quotes.json', 'r') as f:
    quotes = json.load(f)

with open('data/characters.json', 'r') as f:
    characters = json.load(f)

resolutions: List[Dict[str, int]] = [
    {"width": 1280, "height": 720}, # 720p
    {"width": 1920, "height": 1080}, # 1080p
    {"width": 2560, "height": 1440} # 1440p
]

font_path = "static/fonts/ShadowsIntoLight-Regular.ttf"
image_dir = "static/images/"

def scale_character(char_size, scaling_factor):
    char_width, char_height = char_size
    max_width, max_height = 640, 720

    scale = min((max_width / char_width) * scaling_factor, (max_height / char_height) * scaling_factor) # multiply by scaling factor
    
    return (int(char_width * scale), int(char_height * scale))

def generate_image(character, quote, resolution=0): 
    quote_img = Image.new("RGB", tuple(resolutions[resolution].values()))

    scaling_factor = resolution + 1

    char_image_path = os.path.join(image_dir, character["img"])
    char_img = Image.open(char_image_path)
    char_img = char_img.resize(scale_character(char_img.size, scaling_factor))

    char_img_grayscaled = ImageOps.grayscale(char_img)
    quote_img.paste(char_img_grayscaled, (0, 180))

    font_size = 48 * (scaling_factor)

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(quote_img)

    wrapped_quote = textwrap.fill(quote, 30);

    draw.text((200 + (400 * scaling_factor), 100), wrapped_quote, (255, 255, 255), font=font)
    draw.text((200 + (400 * scaling_factor), 600), f"- {character['name']}", (255, 255, 255), font=font)

    img_io = BytesIO()
    quote_img.save(img_io, "PNG")
    img_io.seek(0)
    
    return img_io

if __name__ == '__main__':
    char = next((c for c in characters if c['name'] == 'Goku'), None)
    print(generate_image(char, random.choice(quotes)))
