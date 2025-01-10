import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from uuid import uuid4
import random

with open('data/quotes.json', 'r') as f:
    quotes = json.load(f)

with open('data/characters.json', 'r') as f:
    characters = json.load(f)

font_path = "static/fonts/ShadowsIntoLight-Regular.ttf"
image_dir = "static/images/"
output_dir = "output/"

def scale_character(char_size):
    char_width, char_height = char_size
    max_width, max_height = 640, 720

    scale = min(max_width / char_width, max_height / char_height)
    
    return (int(char_width * scale), int(char_height * scale))

def generate_image(character, quote):
    # generate new blank img
    quote_img = Image.new("RGB", (1280, 720))
    
    image_path = image_dir + character["img"]
    
    # create character img, greyscale and scale it
    char_img = Image.open(image_path)
    char_img = char_img.resize(scale_character(char_img.size))
    char_img_grayscaled = ImageOps.grayscale(char_img)

    # add character
    quote_img.paste(char_img_grayscaled, (0, 180))

    # add quote
    font = ImageFont.truetype(font_path, 48)
    ImageDraw.Draw(quote_img).text((640, 100), quote, (255, 255, 255), font=font)
    ImageDraw.Draw(quote_img).text((640, 400), f"- {character['name']}", (255, 255, 255), font=font)

    # save image
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_path = os.path.join(output_dir, uuid4().hex)
    os.mkdir(output_path)
    quote_path = os.path.join(output_path, "quote.png")
    quote_img.save(quote_path, "PNG")
    
    return quote_path
    
if __name__ == '__main__':
    char = next((c for c in characters if c['name'] == 'Goku'), None)
    print(generate_image(char, random.choice(quotes)))
